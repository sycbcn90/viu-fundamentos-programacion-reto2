# Reto 02: The café order

A Python program for the course Fundamentos de Programación (VIU). It calculates the cost of an order at the university café and shows a receipt in the terminal using the **Rich** library.

## 1. What is the code about?

The café sells three products:

| Product              | Price per unit |
|----------------------|----------------|
| Café (coffee)        | 1.50 EUR       |
| Bocadillo (sandwich) | 3.00 EUR       |
| Zumo (juice)         | 2.00 EUR       |

The program:

1. Asks for the customer's name.
2. Asks how many units of each product the customer wants (0 means they don't want it).
3. Adds up the cost of the whole order (the **subtotal**).
4. If the subtotal is **10 EUR or more**, applies a **10 % discount**. Otherwise, the discount is 0 %.
5. Shows a receipt with a Rich table, the amounts with two decimals, and a coloured message:
   - **Yellow**: no product was chosen.
   - **Green**: the 10 % discount was applied.
   - **Blue**: no discount (it applies from 10 EUR).

## 2. How does the script work?

The script has two parts: calculating the cost and showing the table with Rich.

### Part 1. Total cost calculation

```python
productos = ["Café", "Bocadillo", "Zumo"]
precios = [1.50, 3.00, 2.00]
cantidades = []
```

These are **parallel lists**: the position (the index) links the data. `productos[1]`, `precios[1]` and `cantidades[1]` all belong to the bocadillo. Indexes start at 0.

1. `Prompt.ask(...)` asks for the customer's name and stores it in `nombre_cliente`.
2. A `for i in range(len(productos))` loop goes through positions 0, 1 and 2. On each pass it shows the product and its price.
3. Inside each product there is a `while True` loop. It asks for the quantity with `IntPrompt.ask(...)`, which returns a whole number, and repeats the question until the quantity is valid:
   - **If it is 0**, it asks the customer to confirm (1 = yes, 0 = no) with `IntPrompt.ask`. If the answer is 1, `continue` goes back to the start of the `while` loop and asks for the quantity again. If the answer is 0, it stores a `0` in the list and `break` leaves the loop.
   - **If it is greater than 0**, it stores it with `append` and `break` leaves the loop.
   - **If it is negative**, it shows a warning. Because there is no `break`, the loop asks for the quantity again.

   Each product always ends with an `append`, so `cantidades` has 3 items in the same order as `productos`.
4. A second loop with `zip(precios, cantidades)` goes through each price together with its quantity, calculates `precio * cantidad` and adds it to `subtotal`, which starts at 0.
5. After the loop ends, an `if / else` decides the discount: 10 % of the subtotal if it is 10 EUR or more, and 0 otherwise. Then it calculates `total = subtotal - descuento` and prints it with two decimals.

### Part 2. Table presentation with Rich

- An `if / elif / else` chooses the message with an emoji and a colour: yellow `[yellow]` if the subtotal is 0, green `[green]` if there is a discount, and blue `[blue]` in all other cases.
- A `Table` is created with the columns Café, Bocadillo, Zumo, Subtotal, Descuento, Total and Mensaje esperado, with a light blue header.
- `tabla.add_row(...)` adds one row with the three quantities, the amounts with two decimals (`:.2f`) and the message.
- `console.print(tabla)` shows the table in the terminal.

## Test cases

Enter the quantities in this order: café, bocadillo and zumo.

| Café | Bocadillo | Zumo | Subtotal  | Discount | Total    | Message              |
|------|-----------|------|-----------|----------|----------|----------------------|
| 1    | 1         | 1    | 6.50 EUR  | 0.00 EUR | 6.50 EUR | Blue, no discount    |
| 2    | 1         | 2    | 10.00 EUR | 1.00 EUR | 9.00 EUR | Green, 10 % discount |
| 2    | 2         | 1    | 11.00 EUR | 1.10 EUR | 9.90 EUR | Green, 10 % discount |
| 0    | 0         | 0    | 0.00 EUR  | 0.00 EUR | 0.00 EUR | Yellow, no products  |
| 0    | 3         | 0    | 9.00 EUR  | 0.00 EUR | 9.00 EUR | Blue, no discount    |

The order of exactly 10 EUR gets the discount because the condition is `>=` (greater than **or equal to**).

## Where I used AI

The code is mine. Based on my own code, Claude Code reviewed it and fixed the bugs. Only the lines with errors were changed, and each change is marked in the script with a `# FIX` comment.

| Original code | Fixed Code | Explanation |
|---|---|---|
| `confirma_cliente = Prompt.ask(...)` | `confirma_cliente = IntPrompt.ask(...)` | `Prompt.ask` returns text (`"1"`), which is never equal to the number `1`, so the "yes" answer didn't work. `IntPrompt.ask` returns a whole number. |
| `print("Confirmado, no quieres este producto.")` | `print("Confirmado, no quieres este producto.")`<br>`cantidades.append(0)` | If the 0 wasn't stored, the `cantidades` list became shorter. `zip` then matched quantities with the wrong prices, and `cantidades[2]` caused an `IndexError`. |
| `if confirma_cliente == 1:`<br>`    cantidad_pedido = IntPrompt.ask(...)`<br>`    cantidades.append(cantidad_pedido)`<br>`...`<br>`else:`<br>`    print(...)`<br>`    cantidad_pedido = IntPrompt.ask(...)`<br>`    cantidades.append(cantidad_pedido)` | `while True:`<br>`    cantidad_pedido = IntPrompt.ask(...)`<br>`    if cantidad_pedido == 0:`<br>`        ...`<br>`        if confirma_cliente == 1:`<br>`            continue`<br>`        else:`<br>`            ...`<br>`            cantidades.append(0)`<br>`            break`<br>`    elif cantidad_pedido > 0:`<br>`        cantidades.append(cantidad_pedido)`<br>`        break`<br>`    else:`<br>`        print(...)` | Before, the program asked again only once and stored any value, even a negative number or 0. With `while True` the question repeats until the quantity is valid: `continue` asks again, and `break` leaves the loop once the quantity is stored. |
| `if subtotal >= 10:`<br>`else:`<br>`    total = subtotal` | `if subtotal >= 10:`<br>`    descuento = subtotal * 10 / 100`<br>`else:`<br>`    descuento = 0`<br>`total = subtotal - descuento` | The `if` was inside the `for` loop, so the discount was calculated on every pass. Now it is after the loop. Also, `descuento` didn't exist when the subtotal was under 10, which caused a `NameError` in the table and in the `elif`. With the order 0, 0, 0, `total` didn't exist either. |
| `print(f"Los pedidos son {total} euros en total.")` | `print(f"El total del pedido es de {total:.2f} euros.")` | Without `:.2f` it showed `9.0` instead of `9.00`. |