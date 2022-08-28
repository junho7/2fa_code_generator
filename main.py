from elasticsearch_functions import (
    generate_random_number,
    search_by_keyword,
    update_isblocked_by_id,
    update_issent_by_id,
    reset_issent,
    initial_update_isblocked
)


def main():
    result = generate_random_number()
    print("2FA Code: ", "0x" + result["hits"]["hits"][0]["_source"]["hexadecimal"])
    id = result["hits"]["hits"][0]["_source"]["id"]
    update_issent_by_id(id)


if __name__ == "__main__":
    main()
