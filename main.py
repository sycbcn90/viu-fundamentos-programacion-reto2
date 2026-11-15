# ----------------------------------------
#Part 1. Total cost calculation
# ----------------------------------------
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from rich.console import Console
console = Console()

#create lists
productos = ["Café", "Bocadillo", "Zumo"]
precios = [1.50, 3.00, 2.00]
cantidades = []

#require client name
nombre_cliente = Prompt.ask("Indica tu nombre aquí, por favor")

for i in range(len(productos)):
    producto = productos[i]
    precio = precios[i]
    print(f"Aquí ofrecemos: {producto}. Su precio es de {precio:.2f} euros.")
    while True:
        cantidad_pedido = IntPrompt.ask("¿Nos dices qué cantidad quieres de este producto, por favor?")
        #analyze the order quantity situation
        if cantidad_pedido == 0:
            print("La cantidad del producto es 0. ¿Seguro que no quieres este producto?")
            confirma_cliente = IntPrompt.ask("Por favor, confirma si quieres este producto indicando 1 o 0 (1 significa 'SÍ' y 0 significa 'NO')")
            if confirma_cliente == 1:
                continue          # back to the quantity question
            else:
                print("Confirmado, no quieres este producto.")
                cantidades.append(0)
                break             # next product
        elif cantidad_pedido > 0:
            cantidades.append(cantidad_pedido)
            break                 # next product
        else:
            print("La cantidad del producto es negativa. El sistema solo acepta cantidades iguales o mayores que 0. Por favor, vuelve a introducir la cantidad.")
            # no break: the loop asks again

subtotal = 0
for precio, cantidad in zip(precios, cantidades):
    importe_pedido = precio * cantidad
    subtotal += importe_pedido

# FIX: decide the discount once, after the loop, and always create descuento
if subtotal >= 10:
    descuento = subtotal * 10 / 100
else:
    descuento = 0
total = subtotal - descuento
print(f"El total del pedido es de {total:.2f} euros.")  # FIX: two decimals

# ----------------------------------------
#Part 2. Table presentation with Rich
# ----------------------------------------
if subtotal == 0:
    mensaje = "🤨[yellow]No has elegido ningún producto.[/yellow]"
elif descuento > 0:
    mensaje = "🥳[green]¡Felicidades! Se ha aplicado un descuento del 10 %.[/green]"
else:
    mensaje = "☺️[blue]Gracias por tu compra. El descuento se aplica a partir de 10 euros.[/blue]"
tabla = Table(title="Resumen del pedido", title_style="bold black")
tabla.add_column("Café", header_style="bold black on #ADD8E6")
tabla.add_column("Bocadillo", header_style="bold black on #ADD8E6")
tabla.add_column("Zumo", header_style="bold black on #ADD8E6")
tabla.add_column("Subtotal", header_style="bold black on #ADD8E6")
tabla.add_column("Descuento", header_style="bold black on #ADD8E6")
tabla.add_column("Total", header_style="bold black on #ADD8E6")
tabla.add_column("Mensaje esperado", header_style="bold black on #ADD8E6")
tabla.add_row(
    str(cantidades[0]),
    str(cantidades[1]),
    str(cantidades[2]),
    f"{subtotal:.2f} €",
    f"{descuento:.2f} €",
    f"{total:.2f} €",
    mensaje,
)
console.print(tabla)
