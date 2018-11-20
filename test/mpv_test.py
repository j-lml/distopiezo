import smbus
import math
import time

#device i2c addres
address = 0x68

#registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
smplrt_div = 0x19
config = 0x1a
gyro_config = 0x1b
int_enable = 0x38
accel_xout_h = 0x3b
accel_yout_h = 0x3d
accel_zout_h = 0x3f
gyro_xout_h = 0x43
gyro_yout_h = 0x45
gyro_zout_h = 0x47


def read_bytes(reg):
	return bus.read_bute_data(address, reg)

def read_word(reg):
	h = bus.read_byte_data(address, reg)
	l = bus.read_byte_data(address, reg+1)
	value = (h<<8) +l
	return value

def read_word_i2c(reg):
	val = read_word(reg)
	if(val > 32768):
		return val - 65536
	else:
		return val
	

bus = smbus.SMBus(1)

#device configuration
bus.write_byte_data(address, smplrt_div, 7)
bus.write_byte_data(address, power_mgmt_1, 1)
bus.write_byte_data(address, config, 0)
bus.write_byte_data(address, gyro_config, 24)
bus.write_byte_data(address, int_enable, 1)


while(1):

	print("\n\n\naccel data")
	print(read_word_i2c(0x43)/16384.0)
	print(read_word_i2c(0x45)/16384.0)
	print(read_word_i2c(0x47)/16384.0)

	print("\ngyro data")
	print(read_word_i2c(0x3b)/131.0)
	print(read_word_i2c(0x3d)/131.0)
	print(read_word_i2c(0x3f)/131.0)
	time.sleep(0.1)
