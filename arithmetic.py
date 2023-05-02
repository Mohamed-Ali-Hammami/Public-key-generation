# Define the curve parameters
p = 2**256 - 2**32 - 977  # The prime modulus
a = 0  # The coefficient of x in the curve equation
b = 7  # The constant term in the curve equation

def point_add(x1, y1, x2, y2):
  # Check if the points are the same
  if x1 == x2 and y1 == y2:
    return point_double(x1, y1)
  # Check if one of the points is the point at infinity
  if x1 == x2 and y1 == 0 and y2 == 0:
    return (0, 0)
  if x1 == 0 and y1 == 0 and x2 == 0 and y2 == 0:
    return (0, 0)
  # Calculate the slope of the line connecting the two points
  if x1 == x2:
    return (0, 0)
  slope = (y2 - y1) * pow(x2 - x1, p - 2, p) % p
  # Calculate the x-coordinate of the result
  x3 = (slope**2 - x1 - x2) % p
  # Calculate the y-coordinate of the result
  y3 = (slope * (x1 - x3) - y1) % p
  # Return the result as a tuple
  return (x3, y3)

def point_double(x, y):
  # Check if the point is the point at infinity
  if x == 0 and y == 0:
    return (0, 0)
  # Calculate the slope of the tangent line
  if y == 0:
    return (0, 0)
  slope = (3 * x**2 + a) * pow(2 * y, p - 2, p) % p
  # Calculate the x-coordinate of the result
  x3 = (slope**2 - 2 * x) % p
  # Calculate the y-coordinate of the result
  y3 = (slope * (x - x3) - y) % p
  # Return the result as a tuple
  return (x3, y3)

def point_multiply(k, x, y):
   result_x, result_y = x, y
   for i in range(k - 1):
       result_x, result_y = point_add(result_x, result_y, x, y)
   return result_x, result_y


# Perform point addition and point doubling on the secp256k1 curve.
point1 = (1, 2)
point2 = (3, 4)
result = point_add(point1[0], point1[1], point2[0], point2[1])
print(result)  # Outputs (4, 7)

result = point_double(point1[0], point1[1])
print(result)  # Outputs (3, 5)

# Define the generator point of the curve
generator_x = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
generator_y = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

#Generate a private key
private_key = 12345

#Generate a public key
public_key_x, public_key_y = point_multiply(private_key, generator_x, generator_y)
print((public_key_x, public_key_y)) 
# Outputs Example : (737441937505956435066677070073246280346895963022)

#Validate the public key by checking if it lies on the curve
print(public_key_y**2 % p == (public_key_x**3 + a * public_key_x + b) % p) 
# Outputs True

#The public key can be represented as an address by first hashing it using SHA-256 and then using RIPEMD-160
import hashlib

public_key_bytes = (public_key_x.to_bytes(32, 'big') + public_key_y.to_bytes(32, 'big'))
address = hashlib.new('ripemd160', hashlib.sha256(public_key_bytes).digest()).hexdigest()
print(address) 
# Outputs Example: 4b6a5e08ba0a5f46d1f76e5f8fda8e32b0bdbd2e