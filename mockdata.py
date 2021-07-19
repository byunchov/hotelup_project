import json

with open('/home/bobiyu/Programming/Stage DSS/MOCK_DATA.json', 'r') as f:
    data= json.load(f)

    output = []

    for i, row in enumerate(data):
        row['thumbnail'] = f"room_thumbnails/t{row['number']}.jpg"
        rec = {
            "model": "rooms.room",
            "pk": i + 1,
            "fields": row
        }

        output.append(rec)

    with open('fixture.json', 'w') as out:
        json.dump(output, out)
