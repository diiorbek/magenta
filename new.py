import random

hidden_number = random.randint(1, 100)
attempts = 0

print("🔢 Я загадал число от 1 до 100. Попробуй угадать!")

while True:
    guess = input("Введи число: ")
    
    if not guess.isdigit():
        print("❌ Пожалуйста, введи число!")
        continue

    guess = int(guess)
    attempts += 1

    if guess < hidden_number:
        print("⬆ Больше!")
    elif guess > hidden_number:
        print("⬇ Меньше!")
    else:
        print(f"🎉 Поздравляю! Ты угадал число {hidden_number} за {attempts} попыток!")
        break