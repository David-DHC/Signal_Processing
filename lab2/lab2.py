import numpy as np
import librosa
import soundfile

# Macros
filenames = ["Anduin", "Tirion", "Stormwind", "Saurfang"]
sample_rate = 44100
target_rate = 8000
final_rate = 48000
times = [1, 2, 5, 10]
periods = [30, 15, 6, 3]
truncation_frequency = 3999
spectra = {}
dummy = []

for choice in range(0, 4):
	C = truncation_frequency * times[choice]
	print("")
	print("Choice:", choice + 1, "started")
	print("")
	print("Encoding begins.")
	print("Time per period:", times[choice], "seconds")
	print("Number of periods:", periods[choice])
	print("")
	for period in range(0, periods[choice]):
		print("Encoding period", period + 1, "of", periods[choice], "has started.")
		for filename in filenames:
			# Pre process
			raw_data, sample_rate = librosa.load("./raw/" + filename + ".wav", sr=sample_rate)
			raw_data = raw_data[period * times[choice] * sample_rate : (period + 1) * times[choice] * sample_rate]
			data = librosa.resample(raw_data, sample_rate, target_rate)
			soundfile.write("./pre_processed" + str(times[choice]) + "/" + filename + "/" + str(period) + ".wav", data, target_rate)

			# Encoding
			spectrum = np.fft.fft(data)
			spectrum = spectrum[0:C]
			spectra[filename] = spectrum
			print(filename + "'s encoding successfully finished.")

		first_spectrum = np.append(
							np.append(
								np.append(
									np.append([],
											  spectra["Anduin"]),
									spectra["Tirion"]),
								spectra["Stormwind"]),
							spectra["Saurfang"])

		data_encoded = np.fft.ifft(np.append(first_spectrum, np.conjugate(np.flip(first_spectrum[1:]))))
		data_encoded_real = np.array(dummy)

		for number in data_encoded:
			if abs(number.imag) > 2e-16:
				print(abs(number.imag))
				print("Encoding IFFT: conjugate symmetry failed!")
				exit(0)
		print("Encoding IFFT: conjugate symmetry checked!")

		for number in data_encoded:
			data_encoded_real = np.append(data_encoded_real, number.real)
		soundfile.write("./encoded" + str(times[choice]) + "/" + str(period) + ".wav", data_encoded_real, final_rate)
		print("")

	# Decoding
	print("")
	print("Decoding begins.")
	print("Time per period:", times[choice], "seconds")
	print("Number of periods:", periods[choice])

	altogether_decoded = {"Anduin": np.array(dummy), "Tirion": np.array(dummy), "Stormwind": np.array(dummy), "Saurfang": np.array(dummy)}

	for period in range(0, periods[choice]):
		print("")
		print("Decoding period", period + 1, "of", periods[choice], "has started.")
		data_encoded, final_rate = librosa.load("./encoded" + str(times[choice]) + "/" + str(period) + ".wav", sr=final_rate)
		whole_spectrum_encoded = np.fft.fft(data_encoded)
		for filename_index in range(0,4):
			data_out_first_half = whole_spectrum_encoded[filename_index * C : filename_index * C + C]
			data_out = np.fft.ifft(np.append(data_out_first_half, np.append([0], np.conjugate(np.flip(data_out_first_half[1:])))))
			data_out_real = np.array(dummy)

			for number in data_encoded:
				if abs(number.imag) > 2e-16:
					print(abs(number.imag))
					print(filenames[filename_index] + "Decoding IFFT: conjugate symmetry failed!")
					exit(0)
			print(filenames[filename_index] + "'s decoding IFFT: conjugate symmetry checked!")

			for number in data_out:
				data_out_real = np.append(data_out_real, number.real)
			altogether_decoded[filenames[filename_index]] = np.append(altogether_decoded[filenames[filename_index]], data_out_real)

	soundfile.write("./output" + str(times[choice]) + "/" + "Anduin" + ".wav" , altogether_decoded["Anduin"], target_rate)
	print("Anduin outputted.")
	soundfile.write("./output" + str(times[choice]) + "/" + "Tirion" + ".wav" , altogether_decoded["Tirion"], target_rate)
	print("Tirion outputted.")
	soundfile.write("./output" + str(times[choice]) + "/" + "Stormwind" + ".wav" , altogether_decoded["Stormwind"], target_rate)
	print("Stormwind outputted.")
	soundfile.write("./output" + str(times[choice]) + "/" + "Saurfang" + ".wav" , altogether_decoded["Saurfang"], target_rate)
	print("Saurfang outputted.")
	print("Choice", choice + 1, "completed.")
	print("")
