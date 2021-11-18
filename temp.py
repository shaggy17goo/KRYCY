import detection_rules as dr
import file_handling as gf
import nest_asyncio
    
nest_asyncio.apply() # bez tego się wysypuje na przeglądaniu wielu pcapow 

encodings_list = ['ascii', 'utf_32', 'utf_32_be', 'utf_32_le','utf_16', 'utf_16_be', 'utf_16_le', 'utf_7', 'utf_8', 'utf_8_sig']
my_files = gf.get_files(['/home/mateusz/Documents/test/folder1', '/home/mateusz/Documents/test/folder2' ,'/home/mateusz/Documents/test/folder3'], True, extensions=['json','xml','pcap','txt'])

print('############# IP SCANNING #############')
dr.check_for_ip_address(files=my_files, ip=['51.83.134.233', '10.0.2.5', '213.127.65.23'])
print('\n\n\n######## Structure validation #########')
dr.validate_file_structure(files=my_files)
print('\n\n\n######### Encoding validation #########')
dr.validate_text_encoding(files=my_files, encodings=encodings_list)

# Troche spaghetti code wyszedl w tym detection rules
# Jak sie usunie wypisywanie na konsole to troche lepiej to bedzie wygladalo
# Na evtx trzeba troche poczekac (u mnie paczka ~250 logow to 4min procesowania)
# Do zrobienia jest alertowanie
