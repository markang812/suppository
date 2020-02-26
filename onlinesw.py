def CelsiusToFahrenheit(converted): 
    converted = (temperature * 9/5) + 32
    return converted
def FahrenheitToCelsius(temperature):
    converted = (temperature - 32) * 5/9
    return converted

print("Choose an option:")
print("1: Fahrenheit to Celsius")
print("2: Celsius to Fahrenheit")
case = int(input("Chosen input: "))
temperature = float(input("Input temperature value: "))

if case == 1:
    print(str(FahrenheitToCelsius(temperature)) + "°C")
else: 
    print(str((CelsiusToFahrenheit(temperature)))+ "°F")


