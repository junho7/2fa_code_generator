# 2fa_code_generator
- 2FA Code Generator for 8-digit hexadecimal

# Tech stack
- Python: Script to perform search and update in ElasticSearch
- ElasticSearch: Index for all possible combination of 8-digit hexadecimal code
- MySQL: Generated all possible combination of 8-digit hexadecimal code

# Quick summary
1. `main.py` - Choosing a random code from ElasticSearch. Excluding if it's in blocked list or already sent.
2. `elasticsearch_functions.py` - Searching random code. Updating a doc if it's sent.
3. `query.sql` - Query and procedure to generate the sequential hexadecimal up to 16^8
4. `utils.py` - Connection to MySQL
5. `block_list.py` - List of odd-looking codes, commonly used words, and hexspeak
