from pymongo.errors import PyMongoError


def get_name():
    #  Функція запиту імені кота. Поле обов'язкове.
    while True:
        name = input("Enter cat's name (or press ENTER to exit): ").strip()
        if not name:
            return None
        if len(name) > 0:
            return name
        print("Name cannot be empty.")


def get_age():
    # Функція запиту віку. Поле необов'язкове.
    while True:
        try:
            age_str = input("Enter cat's age as a positive integer value: ").strip()
            if not age_str:
                return None
            age = int(age_str)
            if age < 0:
                print("Age cannot be negative.")
            else:
                return age
        except ValueError:
            print("Invalid value.")


def get_features():
    # Функція запиту особливостей котаю Поле необов'язкове
    features = []
    print("Enter cat's features (leave empty to finish): ")
    while True:
        feature = input(f"Feature {len(features) + 1}: ").strip()
        if not feature:
            break
        features.append(feature)
    return features if features else None


def insert(db):
    """
    Функція вставки одного або декількох записів у колекцію 'cats' переданої у якості
    параметру бази даних PyMongo (db).
    """
    choice = input(
        '\nEnter\t "1" to insert one record\n\t "2" to insert multiple records\n\t Any other input to return to previous menu: '
    ).strip()

    if choice not in ("1", "2"):
        print("Returning to main menu.")
        return

    # Загальний список для вставки
    records_to_insert = []

    if choice == "1":
        print("\nInserting one record\n")
        name = get_name()
        if name is None:
            print("Record insertion cancelled by user choice. Returning to menu.")
            return

        current_record = {"name": name, "age": get_age(), "features": get_features()}
        # В умові наведено схему документа, тому передаємо курент рекорд як є
        # Якщо поля з None не є обов'язковими в схемі - розкоментувати наступний рядок
        # current_record = {k: v for k, v in current_record.items() if v is not None}
        records_to_insert.append(current_record)

    elif choice == "2":
        print("\nInserting multiple records\n")
        while True:
            name = get_name()
            if name is None:
                print("Current record creation cancelled by user choice.")
                if not records_to_insert:
                    print("No records added to queue. Returning to menu.")
                    return
                break

            current_record = {
                "name": name,
                "age": get_age(),
                "features": get_features(),
            }
            # В умові наведено схему документа, тому передаємо курент рекорд як є
            # Якщо поля з None не є обов'язковими в схемі - розкоментувати наступний рядок
            # current_record = {k: v for k, v in current_record.items() if v is not None}
            records_to_insert.append(current_record)
            print(f"Record {current_record} successfully added to queue.")

            while True:
                proceed_choice = (
                    input("Do you want to add another record? (y/n): ").strip().lower()
                )
                if proceed_choice in ("y", "n"):
                    break
                else:
                    print("Incorrect choice. Please enter 'y' or 'n'.")

            if proceed_choice == "n":
                break

    if not records_to_insert:
        print("No records to insert into the database.")
        return

    try:
        if choice == "1":
            result = db.cats.insert_one(
                records_to_insert[0]
            )  # records_to_insert[0] бо він там один
            print(f"Record {records_to_insert[0]} successfully added to database.")
            print(f"Record's ID is: {result.inserted_id}")
        else:
            # Вставка багатьох записів
            result = db.cats.insert_many(records_to_insert)
            print(f"Successfully added {len(result.inserted_ids)} records to database.")
            print(f"Records' IDs are: {result.inserted_ids}")

    except PyMongoError as e:
        print(f"An error occurred during database insertion: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def delete(db):
    # Функція видалення усіх записів або за іменем (в т.ч. усіх записів певного імені)
    initial_choice = input(
        "\nEnter '1' to delete a single record by name\n"
        "\t '2' to delete ALL records from the collection\n"
        "\t Any other input to return to the previous menu: "
    ).strip()

    if initial_choice not in ("1", "2"):
        print("Invalid choice. Returning to main menu.")
        return

    # Видалення усіх записів
    if initial_choice == "2":
        print(
            "\nWARNING: You are trying to delete ALL records from the 'cats' collection!"
        )
        while True:
            confirm_delete_all = (
                input("Are you sure you want to proceed? (y/n): ").strip().lower()
            )
            if confirm_delete_all == "y":
                try:
                    result = db.cats.delete_many({})
                    print(
                        f"Successfully deleted {result.deleted_count} records from 'cats' collection."
                    )
                except PyMongoError as e:
                    print(f"An error occurred during mass deletion: {e}")
                break
            elif confirm_delete_all == "n":
                print("Mass deletion cancelled. Returning to main menu.")
                break
            else:
                print("Incorrect choice. Please enter 'y' or 'n'.")
        return

    # Видалення за іменем
    elif initial_choice == "1":
        name_to_delete = get_name()
        if name_to_delete is None:
            print(
                "Deletion by name cancelled by user`s choice. Returning to main menu."
            )
            return

        try:
            # Спочатку дивимся кількість записів з певним іменем

            count = db.cats.count_documents({"name": name_to_delete})

            # Якщо випадків більше одного надаємо вибір, чи видаляти всі чи лише перший у базі
            if count > 1:
                print(
                    f"More than one record with name '{name_to_delete}' was found ({count} records)."
                )
                decision_choice = (
                    input(
                        "Delete all records with this name? ('y' - delete all, 'n' - delete only the first, any other input to cancel): "
                    )
                    .strip()
                    .lower()
                )

                match decision_choice:
                    case "y":
                        result = db.cats.delete_many({"name": name_to_delete})
                        print(
                            f"Successfully deleted {result.deleted_count} records with name '{name_to_delete}'."
                        )
                    case "n":
                        result = db.cats.delete_one({"name": name_to_delete})
                        print(
                            f"Successfully deleted one record with name '{name_to_delete}'."
                        )
                    case _:
                        print(
                            "Deletion cancelled by user`s choice. Returning to main menu."
                        )
                        return
            # Якщо запис лише один - видаляємо його
            elif count == 1:
                result = db.cats.delete_one({"name": name_to_delete})
                print(f"Successfully deleted one record with name '{name_to_delete}'.")
            # Якщо записів з наданим іменем не знайдено
            else:
                print(f"No record named '{name_to_delete}' was found.")

        except PyMongoError as e:
            print(f"An error occurred during deletion: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


def update(db):
    # Функція оновлення значень віку або особливостей за іменем кота
    name = get_name()

    if name is None:
        print("Update cancelled by user. Returning to menu.")
        return

    try:
        # Рахуємо кількість записів з даним іменем
        matching_count = db.cats.count_documents({"name": name})

        if matching_count == 0:
            print(f"Record named '{name}' was not found in 'cats' collection.")
            return

        # У разі виявлення декількох записів з одним іменем запитуємо вибір користувача
        target = {"name": name}
        is_update_all = False

        if matching_count > 1:
            print(f"Found {matching_count} records with name '{name}'.")
            choice_multiple = (
                input(
                    "Do you want to update ALL of them? ('y' - update ALL, 'n' - update only first found): "
                )
                .strip()
                .lower()
            )

            if choice_multiple == "y":
                is_update_all = True
            elif choice_multiple == "n":
                pass  # target залишаємо без змін
            else:
                print("Incorrect choice. Update cancelled.")
                return

        # SВстановлюємо, що саме будемо оновлювати - ім'я чи властивості
        decision_choice = (
            input(
                "\nWhat do you want to update in records named '" + name + "'?\n"
                "\t 'a' - update age\n"
                "\t 'f' - update features\n"
                "\t any other input - cancel update: "
            )
            .strip()
            .lower()
        )

        update_data = {}

        match decision_choice:
            case "a":
                age = get_age()
                if age is not None:
                    update_data["age"] = age
                else:
                    print("Update cancelled by user.")
                    return
            case "f":
                new_features = get_features()
                if new_features is not None:
                    update_data["features"] = new_features
                else:
                    print("Features update cancelled by user.")
                    return
            case _:
                print(f"Update of record named {name} cancelled by user.")
                return

        # Перевірка, чи наявні дані для оновлення
        if not update_data:
            print("The data to update was not found. Update cancelled.")
            return

        # Власне оновлення з врахуванням вибору одиночного чи множинного оновлення
        if is_update_all:
            result = db.cats.update_many(target, {"$set": update_data})
            print(f"{result.modified_count} records named'{name}' succesfully updated.")
        else:
            result = db.cats.update_one(target, {"$set": update_data})
            if result.modified_count > 0:
                print(f"Record named '{name}' succesfully updated.")
            else:
                print(f"Record named '{name}' was found, but was not updated.")

    except PyMongoError as e:
        print(f"Unexpected error during database updating: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def read(db):
    # Функція перегляду всієї бази або перегляду за іменем
    decision_choice = (
        input(
            "\nDo you want to read all records in 'cats' collection or records with a specified name?\n"
            "\t 'a' - read all\n"
            "\t 'n' - read by name\n"
            "\t Any other input to cancel: "
        )
        .strip()
        .lower()
    )
    result = None
    try:
        match decision_choice:
            case "a":
                print("\nReading all records")

                result = db.cats.find({})

            case "n":
                print("\nReading records by name")
                name = get_name()
                if name is None:
                    print(
                        "Database reading cancelled by user`s choice. Returning to menu."
                    )
                    return

                result = db.cats.find({"name": name})

            case _:
                print("Database reading cancelled. Returning to menu.")
                return
        # Виведення результатів пошуку
        if result is not None:
            found_records_count = 0
            for record in result:
                print(record)
                found_records_count += 1

            if found_records_count == 0:
                if decision_choice == "a":
                    print("Were are not found noone records in the 'cats' collection.")
                else:
                    print(f"ЗRecords named'{name}' were not found.")
            else:
                print(f"Found and printed: {found_records_count} record(s).")

    except PyMongoError as e:
        print(f"An error occurred during database reading: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
