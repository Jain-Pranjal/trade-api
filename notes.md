as we are using the pydantic setting so it will self read the .env file and load the variables from there
so there is **NO NEED** to use load_dotenv from dotenv package

- Pydantic Settings automatically .env file load karta hai - aapko manually load_dotenv() call karne ki zarurat nahi hai.



'''
pre-commit hooke apake basically git hooks me add hot ahia so we need to install that also so that vo apake hooks me register ho jaye basiclly apak jo git hooks hote hi precomit ke hooks apke un gith ub hke hoks ke sath miltehai and then vo aapna kamakrtehai in pythn proejct ke ander
'''


we need to install pre-commit package so that we can use pre-commit hooks in our project
uv add pre-commit
<!-- this will only add the package but wee need to install the hooks  -->
pre-commit install
