from website.helpers.historie_handling import get_user_zkouseni_historie, save_to_user_zkouseni_historie

def check_if_historie_updated_or_update() -> None:
	file = get_user_zkouseni_historie()
	if len(file) == 0:
		print("slovník je prázdnej, takže bude fungovat s novejma ID")
		pass
	else:
		try:
			x = file[0]["id"]
			print("slovník už běží pomocí ID")
		except KeyError:
			print("updatuju slovník na verzi s ID")
			id = 0
			for zaznam in file:
				zaznam["id"] = id
				id += 1
			save_to_user_zkouseni_historie(file)