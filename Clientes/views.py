import json
from django.shortcuts import render
from django.db.models import Q

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect, render
from Clientes.forms import createClientForm
from db.models import Cliente, User
# Create your views here.

# Create your views here.

from django.contrib.auth.decorators import user_passes_test,login_required

@login_required(login_url='authentication:login')
def clientesIndex(request):
    return render(request, 'Clientes/indexClientes.html')


def clientsCard(request):
    jsonObject = json.load(request)['jsonBody']
    search = jsonObject["search"]    
    employees = Cliente.objects.filter(is_active=True)
    if search != "":
        employees = employees.filter(
            Q(nombre__icontains=search) 
        )

  
    return render(request, "Clientes/clienteCard.html",{'employees':employees})

@login_required(login_url='authentication:login')

def clientesEditar(request,id):
    user = Cliente.objects.get(id=id)
    if request.method == "POST":
        form = createClientForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
                user = form.save()
                user.save()

                return redirect("Clientes:clientesIndex")
        else:
                return render(request, 'Clientes/editarCliente.html',{'form':form, 'user':user})


    form = createClientForm(instance=user)
    print(user)
    return render(request, 'Clientes/editarCliente.html',{'form':form,'user':user})

@login_required(login_url='authentication:login')

def clientesEliminar(request,id):
    clientes = Cliente.objects.get(id=id)
    print(clientes)
    clientes.is_active=False
    clientes.save()
    return redirect("Clientes:clientesIndex")


@login_required(login_url='authentication:login')
def clientesCrear(request):
    if request.method == "POST":
        form = createClientForm(request.POST, request.FILES)
   
        if form.is_valid():
            user = form.save()
            user.save()
            


            
            return redirect("Clientes:clientesIndex")
        else:
            return render(request, 'Clientes/crearCliente.html',{'form':form})
          

    form = createClientForm()

    return render(request, 'Clientes/crearCliente.html',{'form':form})


