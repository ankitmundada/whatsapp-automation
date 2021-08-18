
The template uses column names of the input csv

Steps:

1. Run `pip install selenium tqdm webdriver_manager`
2. Update the template
3. Run the below command 


*Command*
```
python whatsapp.py --template message.template --data dotpe-sellers-data-results.cs
```

Results are written to a file in a new file in the same folder.
- Checkout the last column called `is_sent` in the output file to know message status


---

Tested with python v3.7

