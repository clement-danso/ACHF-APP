
import gspread


gc = gspread.service_account()

sh = gc.open("ODK Phone contacts")


print(gc)
worksheet=sh.sheet1
contact_list = worksheet.col_values(1)

#print(worksheet.get('A1'))
print(contact_list)
