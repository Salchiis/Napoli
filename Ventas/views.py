import datetime
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from Ventas.forms import VentaMenuForm, createVentaForm, modifyMesaForm, modifyVentaForm
from db.models import Cliente, Menu, Mesa, User, Venta, VentaMenu,Extras
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.decorators import user_passes_test,login_required
from django.http import QueryDict
from decimal import Decimal
import re

def isAdmin(user):
    if user.rol == 'Admin':
        return True
    else:
        return False
    


@login_required(login_url='authentication:login')
# Create your views here.
def ventasIndex(request):
    form = createVentaForm()
    form2 = modifyVentaForm()
    form3 = modifyMesaForm()
    ventas = Venta.objects.filter(is_open=True).order_by('-fecha_compra')
    user = request.user

    return render(request, 'Ventas/indexVentas.html',{'form':form,'ventas':ventas,'form2':form2,'form3':form3,'user':user})

@login_required(login_url='authentication:login')

def addCliente(request,id):
    venta = Venta.objects.get(id=id)
    if request.method == 'POST':
        form = modifyVentaForm(request.POST, instance=venta)  # Inicializar el formulario con los datos POST
        if form.is_valid():
            user = form.save()
            user.save()
        else:
            return redirect('Ventas:modificarVenta',id)

    return redirect('Ventas:modificarVenta',id)


def addMesa(request,id):
    venta = Venta.objects.get(id=id)
    if request.method == 'POST':
        form = modifyMesaForm (request.POST, instance=venta)  # Inicializar el formulario con los datos POST
        if form.is_valid():
            user = form.save()
            user.save()
        else:
            print(form.errors)
            return redirect('Ventas:modificarVenta',id)

    return redirect('Ventas:modificarVenta',id)

def addRow(request, id):
    venta = Venta.objects.get(id=id)
  

    nueva_mesa = 'Para llevar' 

    response_data = {'mensaje': 'Actualización exitosa'}
   
    
    return JsonResponse(response_data)


def clienteRow(request):
    
    jsonObject = json.load(request)['jsonBody']
    search = jsonObject["search"]    
    clientes = Cliente.objects.filter(is_active=True)
    if search != "":
        clientes = clientes.filter(
            Q(nombre__icontains=search) 
        )
    return render(request, "Ventas/clienteRow.html",{'clientes':clientes})


def menuRow(request):
    
    jsonObject = json.load(request)['jsonBody']
    search = jsonObject["search"]    
 
    menus = Menu.objects.all()
    if search != "":
        menus = menus.filter(
            Q(nombre__icontains=search) 
        )
    return render(request, "Ventas/menuRow.html",{'menus':menus})


def menuRow2(request):
    
    jsonObject = json.load(request)['jsonBody']
    search = jsonObject["search"]    
 
    menus = Menu.objects.filter(categoria='Pizza')
    if search != "":
        menus = menus.filter(
            Q(nombre__icontains=search) 
        )
    return render(request, "Ventas/menuRow2.html",{'menus':menus})

@login_required(login_url='authentication:login')

def modificarVenta(request,id):
    menu = Menu.objects.all()

    venta = Venta.objects.get(id=id)
    mesas = Mesa.objects.all()
    lista = VentaMenu.objects.filter(venta=id)
    user = request.user
    total2 = 0
    for total in lista:
        total2 += total.totalfinal
    venta.total = total2
    venta.save()
    form = modifyVentaForm(instance=venta)
    form2 = VentaMenuForm()
    form3 = modifyMesaForm()

    return render(request, 'Ventas/modificarVentas.html',{'venta':venta,'lista':lista,'form':form,'form2':form2,'form3':form3,'total':total2,'user':user,'mesas':mesas,'menu':menu})



@login_required(login_url='authentication:login')

def cerrarVenta(request,id):
    venta = Venta.objects.get(id=id)
    cliente = venta.cliente
    lista = VentaMenu.objects.filter(venta=id)
    
    total2 = 0
    for total in lista:
        total2 += total.totalfinal
    venta.total = total2
    venta.save()
    

    #if venta.is_reopen == False:
    #    cliente.total_compras +=  1
    #    cliente.total_gastado += total
    #cliente.save()
    
    venta.is_reopen = True
    venta.is_open= False
    venta.save()
    
    
    return redirect('Ventas:ventasIndex')
@login_required(login_url='authentication:login')

def abrirVenta(request,id):
    venta = Venta.objects.get(id=id)
    venta.is_open= True
    if not venta.is_reopen:
        venta.is_reopen= True
  

    venta.save()
    return redirect('Ventas:ventasIndex')




@login_required(login_url='authentication:login')

def agregarVenta(request, id):
    ventas = Venta.objects.get(id=id)
    lista = VentaMenu.objects.filter(venta=id)
    data_from_jquery = request.POST
    mutable_data = QueryDict(mutable=True)
    mutable_data.update(data_from_jquery)
    new_dict = {re.sub(r'_\d+$', '', key): value for key, value in mutable_data.items()}
    print(new_dict)
    if request.method == "POST":
        menu_id = new_dict.get('id_menu')
        cantidad = Decimal(new_dict.get('id_cantidad'))
        observaciones = new_dict.get('id_observaciones')
        pizza_id = new_dict.get('id_pizza_mitad')
        familiar = new_dict.get('id_familiar')
        media_orden = new_dict.get('id_media_orden')
        extra1=new_dict.get('id_extras_0')
        extra2=new_dict.get('id_extras_1')
        extra3=new_dict.get('id_extras_2')
        extra4=new_dict.get('id_extras_3')
        extrasList = [extra1, extra2, extra3, extra4]

        menu = None
        pizza_mitad = None
        for i in range(len(extrasList)):
            extrasList[i] = extrasList[i] != "false"
           
        if media_orden == "false":
            media_orden = False
        else:
            media_orden = True
        if familiar == "false":
            familiar = False
        else:
            familiar = True
        if menu_id:
            menu = Menu.objects.get(id=menu_id)
        
        if pizza_id:
            pizza_mitad = Menu.objects.get(id=pizza_id)
        #####
  

        total = 0
       

        if menu.categoria == "Pizza":
            if familiar:
                if pizza_mitad:
                    if pizza_mitad.precioFamiliar < menu.precioFamiliar:
                        total += (menu.precioFamiliar) * cantidad
                    else:
                        total += (pizza_mitad.precioFamiliar) * cantidad
                else:
                    total += (menu.precioFamiliar) * cantidad
            else:
                if pizza_mitad: 
                    if pizza_mitad.precio < menu.precio:
                        total += (menu.precio) * cantidad
                    else:
                  
                        total += (pizza_mitad.precio) * cantidad
                else:
                        total += (menu.precio) * cantidad
        elif media_orden == True: #Mediaorden
                total += (menu.mediaOrden) * (cantidad)

        else: #Compra normal
                total += (menu.precio) * cantidad
        print(total,"antes de extras")
        listaextras = Extras.objects.all()
        
        for i,ext in enumerate(listaextras):
            if extrasList[i] == True:
                if familiar:
                    total += ext.precioFamiliar * cantidad
                else:
                    total += ext.precio * cantidad
        indicies = []
        for i,ex in enumerate(extrasList):
            elemento = Extras.objects.get(id=i+1)
            if extrasList[i] == True:
                    indicies.append(i+1)
      

        queryset_result = Extras.objects.filter(id__in=indicies)        
       
        print(total)
        ####   
        form = VentaMenuForm({
            'venta': ventas,
            'menu': menu,
            'cantidad': cantidad,
            'observaciones': observaciones,
            'familiar': familiar,
            'media_orden': media_orden,
            'pizza_mitad': pizza_mitad,
            'totalfinal':total,
            'extras':queryset_result,
            'final':total
        })

        if form.is_valid():    
            data = form.cleaned_data
            data2 = form.save()
            return redirect("Ventas:modificarVenta", id)
        else:
            print(form.errors)
    return redirect("Ventas:ventasIndex")


@login_required(login_url='authentication:login')

def ventasCrear(request,id):
    if request.method == "POST":
        form = createVentaForm(request.POST, request.FILES)
   
        if form.is_valid():
            user = form.save()
            user.empleado = User.objects.get(id=id)
            user.cliente = Cliente.objects.get(id=1)

            user.is_open = True
            user.save()
                      

            
            return redirect("Ventas:ventasIndex")
        else:
            return render(request, 'Ventas/ventasIndex.html',{'form':form})
          

    form = createVentaForm()

    return redirect("Ventas:ventasIndex")
@login_required(login_url='authentication:login')

def ventasTodas(request):



    return render(request, 'Ventas/ventasTodas.html',)

def ventasCard(request):
    jsonObject = json.load(request)['jsonBody']
    search = jsonObject["search"]    
    fecha = jsonObject["date"]
   
    
    ventas = Venta.objects.filter(is_open=False).order_by('-fecha_compra')

    if fecha != "":
        if fecha != "" :
            date = fecha.split("/")
            start_dt = datetime(int(date[2]), int(date[1]), int(date[0]))
            ventas = ventas.filter(
                Q(fecha_compra__date=start_dt)  
            )

                
    return render(request, "Ventas/ventasCard.html",{'ventas':ventas})

@login_required(login_url='authentication:login')
def guardarCambios(request,compra_id,list_id,operacion):

    venta = Venta.objects.get(id=compra_id)
    producto = VentaMenu.objects.get(venta=venta,id=list_id)

    if operacion == "suma":
        
        producto.cantidad = producto.cantidad + 1
        producto.totalfinal = producto.final * producto.cantidad
        producto.save()

    else:
        
        if producto.cantidad > 0:
                producto.cantidad = producto.cantidad - 1
                producto.totalfinal = producto.final * producto.cantidad
                producto.save()
        if producto.cantidad == 0:
                producto.delete()
   
       

        
        
    
    return redirect("Ventas:modificarVenta",compra_id)
@login_required(login_url='authentication:login')

def cambiarFactura(request,id):
        compras = Venta.objects.get(id=id)
        if compras.bool_factura == True:
            compras.bool_factura = False
            compras.save()
        else:
            compras.bool_factura = True
            compras.save()

        return redirect("Ventas:modificarVenta",id)
