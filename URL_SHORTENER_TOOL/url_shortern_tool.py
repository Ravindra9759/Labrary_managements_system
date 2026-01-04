import uuid
import hashlib
url_store  = {}

def generate_slug(url : str) -> str:
    unique_str = url + str(uuid.uuid4())
    slug = hashlib.sha256(unique_str.encode()).hexdigest()[:8]
    return slug

def shorten_url(url : str) -> str:
    if not url.strip():
        return "❌ Error : URL connot be empty"
    if url in url_store.values():
        for slug, stored_url in url_store.items():
            if stored_url == url:
                return f" Already shortened : {slug}"
    slug = generate_slug(url)
    url_store[slug] = url
    return f" Short URL created : {slug}"

def retrieve_url(slug : str) -> str:
    return url_store.get(slug, "❌ Error : Slug not found")

def menu():
    while True:
        print("\n URL Shortener CLI ")
        print("1. Shorten URL")
        print("2. Retrieve URL")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            url = input("Enter the Original URL: ")
            print(shorten_url(url))
        elif choice == "2":
            slug = input("Enter the Slug: ")
            print(retrieve_url(slug))
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("❌ Invalid choice. Try again.")
if __name__ == "__main__":
    menu()

        
