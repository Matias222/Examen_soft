from fastapi import FastAPI, Query, HTTPException
from typing import List

from datetime import datetime

app = FastAPI()

arreglo_usuario={} #Hashmap para O(1) en lugar de O(n) por query

def get_date():
    current_date = datetime.now()

    # Get the day and month from the current date
    day = str(current_date.day)
    month = str(current_date.month)
    year = str(current_date.year)

    return day+"-"+month+"-"+year


@app.get("/billetera/contactos")
def get_contactos(minumero: str = Query(...)):

    if(minumero not in arreglo_usuario): raise HTTPException(status_code=404, detail="User not found")

    user_temp=arreglo_usuario[minumero]

    devolver = user_temp.get_contactos()

    if(devolver=="Contacto no existente"): raise HTTPException(status_code=404, detail="Contacto not found")

    return devolver

@app.get("/billetera/pagar")
def get_contactos(minumero: str = Query(...), numerodestino: str=Query(...), valor:float=Query(...)):
    if(minumero not in arreglo_usuario): raise HTTPException(status_code=404, detail="User not found")

    user_temp=arreglo_usuario[minumero]

    devolver=user_temp.pagar(numerodestino,valor)

    if(devolver=="No en contactos"): raise HTTPException(status_code=404, detail="Contacto not found")
    elif(devolver=="Insuficiente"): raise HTTPException(status_code=500, detail="Not enough funds")
    
    print(devolver)

    return devolver

@app.get("/billetera/historial")
def get_contactos(minumero: str = Query(...)):

    if(minumero not in arreglo_usuario): raise HTTPException(status_code=404, detail="User not found")

    user_temp=arreglo_usuario[minumero]
     
    datos=user_temp.get_historial()
    devolver={}

    for i in range(len(datos)):
        devolver[i]=datos[i]
        print(datos[i])
    print(devolver)
    return devolver

class Operacion():

    
    ejecutante: str
    fecha:datetime
    valor:float
    is_receptor:bool

    def __init__(self,ejecutante,fecha,valor,is_receptor):
        self.ejecutante=ejecutante
        self.is_receptor=is_receptor
        self.fecha=fecha
        self.valor=valor


class Cuenta():
    numero:str
    nombre:str
    saldo:float
    contactos: List[str]=[]
    historial: List[Operacion]=[]

    def __init__(self,numero,nombre,saldo,contactos):
        self.nombre=nombre
        self.numero=numero
        self.saldo=saldo
        self.contactos=contactos
        self.historial=[]

    def __str__(self):
        return f"Numero: {self.numero}\nNombre: {self.nombre}\nContactos: {', '.join(self.contactos)}"

    def get_contactos(self):
        datos={}

        print("Contactos de",self.numero)

        for i in self.contactos: 
            
            if (i not in arreglo_usuario): return "Contacto no existente"

            contacto_temp=arreglo_usuario[i]
            
            datos[contacto_temp.numero]=contacto_temp.nombre
            
            print(contacto_temp.numero,contacto_temp.nombre)
        
        return datos

    def agregar_transaccion(self,destino,monto,flag):
        self.historial.append(Operacion(destino,datetime.now(),monto,flag))

    def pagar(self,destino,monto):
        
        if(destino not in self.contactos): return "No en contactos"

        if(monto>self.saldo): return "Insuficiente"

        print(self.historial)

        self.saldo=self.saldo-monto

        destino_temp=arreglo_usuario[destino]

        destino_temp.saldo+=monto
        destino_temp.agregar_transaccion(self.numero,monto,1)
        
        print(self.historial)

        self.historial.append(Operacion(destino,datetime.now(),monto,0))
        
        return {"info":"Realizado en "+get_date()}

    def get_historial(self):
        
        datos=[]

        print(self.historial)

        for i in self.historial:
            cadena="Pago "
            primera=""
            segunda=""
            if(i.is_receptor==0): 
                primera="realizado "
                segunda=" a "
            else: 
                primera="recibido "
                segunda=" de "

            cadena=cadena+primera+"de "+str(i.valor)+segunda+i.ejecutante
    
            datos.append(cadena)
        
        return datos

arreglo_usuario["1"]=Cuenta("1","Matias",200,["2","3"])
arreglo_usuario["2"]=Cuenta("2","Gabriel",300,["1","3"])
arreglo_usuario["3"]=Cuenta("3","Juan",400,["1","2"])

