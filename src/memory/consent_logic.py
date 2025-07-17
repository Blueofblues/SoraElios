def consent_to_remember(entry_title, user_confirmed):
	if user_confirmed:
		return f"Memory '{entry_title}' has been stored with care."
	else:
		return f" Memory '{entry_title}' has been released with grace."

