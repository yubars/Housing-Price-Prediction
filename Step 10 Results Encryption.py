from cryptography.fernet import Fernet
# Message to encrypt
house_price = "340500"
equity_value = "115030"
house_price_per_sqft = "11.5"

# Generating the Key
key = Fernet.generate_key()
fernet = Fernet(key)

print(f"Key: {key}")

# Encrpyting the messages
enc_house_price = fernet.encrypt(house_price.encode())
enc_equity_value = fernet.encrypt(equity_value.encode())
enc_house_price_per_sqft = fernet.encrypt(house_price_per_sqft.encode())
print("Original House Price: ", house_price)
print("Encrypted House Price: ", enc_house_price)
print("Original Equity Value: ", equity_value)
print("Encrypted Equity Value: ", enc_equity_value)
print("Original House Price Per Sqft: ", house_price_per_sqft)
print("Encrypted House Price Per Sqft: ", enc_house_price_per_sqft)

# Decrypting the messages
dec_house_price = fernet.decrypt(enc_house_price).decode()
dec_equity_value = fernet.decrypt(enc_equity_value).decode()
dec_house_price_per_sqft = fernet.decrypt(enc_house_price_per_sqft).decode()
print("Decrypted House Price: ", dec_house_price)
print("Decrypted Equity Value: ", dec_equity_value)
print("Decrypted House Price Per Sqft: ", dec_house_price_per_sqft)
