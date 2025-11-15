def main():
    try:
        weight = float(input("Enter weight in kg: "))
        height = float(input("Enter height in meters: "))
        if weight <= 0 or height <= 0:
            print("Invalid input. Weight and height must be positive.")
            return
        bmi = weight / (height ** 2)
        print(f"Your BMI is {bmi:.2f}")
        if bmi < 18.5:
            print("Underweight")
        elif bmi < 25:
            print("Normal weight")
        elif bmi < 30:
            print("Overweight")
        else:
            print("Obese")
    except ValueError:
        print("Invalid input. Please enter numbers.")

if __name__ == "__main__":
    main()
