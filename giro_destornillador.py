#giro de destornillador
#motores 4 y 5
import pigpio
import time
pi=pigpio.pi()
#motor 4
d4=7
e4=12
#motor 5
d5=16
e5=20

#apagar todos los motores
for a in [12,20,7,16]:
    pi.write(a,0)

time.sleep(1)

for a in [12,20]:
    pi.write(a,0)

time.sleep(4)
for a in [7,16]:
    pi.write(a,1)

time.sleep(4)
for a in [12,20]:
    pi.write(a,1)

print('fin')