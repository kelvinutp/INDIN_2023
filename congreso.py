import pigpio
import time

pi=pigpio.pi()

class gryphon:
    def __init__(self,dire,ena,enca,encb,rango,ls=[],clk=18,freq=1000):
        """
        dire=   GPIO direccion\n
        ena=    GPIO enable\n
        enca=   GPIO encoder A\n
        encb=   GPIO encoder B\n
        rango=  la totalidad de rango angular disponible
        ls    GPIO limit switches (maximo 2)\n
	clk= GPIO that will carry clock signal\n
	freq= frequency in Hz of the clock cycle, default a 50% duty cycle\n
        """
        self.dire=dire
        self.ena=ena
        self.ls=ls
        self.enca=enca
        self.encb=encb
        self.estado={}
        self.rango=rango


        self.ls_anterior=0

        self.current_angle=360 #search for 0 degree position
        self.total_angle=0
        self.factor=0 #conversion factor
        
        sali=[self.dire,self.ena]
        entr=[self.enca,self.encb]

        for a in sali:
            pi.set_mode(a,pigpio.OUTPUT)
            pi.write(a,True)
            self.estado[a]=True
        
	#for limit switches, configure input pin and callout function
        for a in self.ls[:2]:
            pi.set_mode(a,pigpio.INPUT)
            pi.callback(a,pigpio.PUD_DOWN)
            pi.callback(a,0,self.__limit)

        #para encoders, configuracion de pines de entrada y funcion de llamada
        for a in entr:
            pi.set_mode(a,pigpio.INPUT)
            pi.callback(a,pigpio.PUD_DOWN)
            pi.callback(a,0,self.__encoder)

        #set clock signal
        pi.set_mode(18,pigpio.ALT5)
        pi.write(18,0)
        time.sleep(3)
        pi.set_PWM_frequency(clk,freq)
        pi.set_PWM_dutycycle(clk,128)
    #pi.hardware_PWM(clk,1000,500000)
            
    def show_GPIO(self):
        """
        Muestra los pines GPIO y sus respectivas conexiones
        """
        print("GPIO de direccion: ",self.dire)
        print("GPIO de enable:    ",self.ena)
        print("GPIO de encoder A: ",self.enca)
        print("GPIO de encoder B: ",self.encb)
        if len(self.ls)!=0:
            for a in self.ls:
                print('GPIO de limit switch:', a)
        #print('\n')
        #print('\n')
    
    def show_state(self):
        """
        Muestra el estado (True(1)/False(0)) de los GPIO
        """
        for a,b in self.estado.items():
            print("GPIO: {:>2}, Estado: {:<5}".format(a,b))
        print()
    
    def change(self,control,state):
        """
        control ("dir"/"ena")
        state(True/False)
        """
        if control.lower()=='dir':
            pin=self.dire
        elif control.lower()=='ena':
            pin=self.ena
        pi.write(pin,state)
        self.estado[pin]=state
        return
    
    def __limit(self,p,e,t):

        if self.ls_anterior!=p:
            if self.estado[self.dire]:
                self.current_angle=0
            else:
                self.total_angle=self.current_angle
            #cambia la direccion
            self.change('dir',not(self.estado[self.dire]))

            self.ls_anterior=p
        
        #detiene el enable
        self.change('ena',True)
        pi.write(self.ena,True)
        return
    
    def __encoder(self,p,e,t):
        # print(p)
        # if self.enca and not(self.encb):
        if self.encb and self.estado[self.dire]:
            self.current_angle-=1
        else:
            self.current_angle+=1

        return

    def calibracion(self):
        
        if len(self.ls)<=1:
            print("no se puede realizar un correcto proceso de calibracion, por solo tener 1 interruptor limite (limit switch)")
        else:
            self.show_state()

            print("proceso de calibracion, buscando angulo 0 (inicio)")
            while self.current_angle!=0:
                self.change('ena',False)
                print('Grados actuales: ',self.current_angle)
            print(time.time())
            
            self.show_state()
            print('cambio de direccion, buscando maximo angulo (fin)')
            while self.total_angle==0:
                self.change('ena',False)
                # print('Grados actuales: ',self.current_angle)
            
            self.show_state()
            print('Proceso de calibracion finalizado')
            print(time.time())

            print('Total de pulsos: ',self.total_angle)
            self.factor=self.total_angle/self.rango
            print('Factor de conversion: ',self.factor)
            
            #finaliza en "medio" de recorrido
            while self.current_angle>=(self.total_angle*0.5):
                # print('Grados actuales: ',self.current_angle)
                self.change('ena',False)
            
            print('Ticks actuales: ',self.current_angle)
            print('Grados actuales: ',self.current_angle/self.factor)

            self.change('ena',True)
            print()

    def move(self,grados=0,w='cw',varia=False,step=0):
        '''
        grados=cantidad de grados a mover
        w= sentido de movimiento (CW) horario o (CCW)antihorario
        varia(True/False)= hacer movimiento con variacion de frecuencia
        step= cantidad de pasos a mover el brazo. 1.8grados/pasos para los motores actuales
        '''
        if step!=0 and grados==0:
            grados=step*1.8

        c=grados*self.factor

        if w.lower()=='ccw':
            print('sentido antihorario')
            self.change('dir',True)
            target=self.current_angle-c
            print('Actual: ',self.current_angle,'Destino: ',target)
            self.change('ena',False)
            while self.current_angle>=target:
                pass
        elif w.lower()=='cw':
            print('sentido horario')
            self.change('dir',False)
            target=self.current_angle+c        
            print('Actual: ',self.current_angle,'Destino: ',target)
            self.change('ena',False)
            while self.current_angle<=target:
                pass
        self.change('ena',True)
        print('Grados actuales: ',self.current_angle/self.factor)

    def variador (self, incremento=10,atraso=1):
        """
        incremento: delta frecuencia para incrementar/decrementar la frecuencia
        atraso (segundos): cuando tiempo demora en subir/bajar al siguiente escalon
        """
        print('se dara un incremento de: ', incremento)
        #incremento
        f_min=500
        f_max=1000
        for a in range(f_min,f_max+1,incremento):
            pi.hardware_PWM(18,a,500000)
            time.sleep(atraso)
        
        #mantener frecuencia
        time.sleep(5)

        #decremento
        for a in range(f_max,f_min-1,-incremento):
            pi.hardware_PWM(18,a,500000)
            time.sleep(atraso)
        
        return



if __name__=="__main__":
    try:
        m1=gryphon(14,15,2,3,270,[6,13])
        time.sleep(1)
        #m2=gryphon(23,24,4,17,165,[19,26])
        #m3=gryphon(25,8,13,15,300,[21])
        m1.show_GPIO()
        #m2.show_GPIO()
        #m3.show_GPIO()
        m1.calibracion()
        # m2.calibracion()

        # time.sleep(10)
        # print('se moveran 30 grados sentido antihorario')
        m1.move(30,'ccw')

        # time.sleep(2)
        # print('se moveran 90 grados sentido antihorario')
        m1.move(90,'cw')
        time.sleep(2)
        m1.variador(25,2)


    except KeyboardInterrupt:
        m1.change('ena',True)
        print('\nPrograma interrumpido')

pi.hardware_PWM(18,0,0)
pi.write(18,0)

#proyecto de congreso INDIN
