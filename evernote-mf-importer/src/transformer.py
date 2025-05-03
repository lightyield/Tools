def transform_notes(titles):
    records = []
    errors = []

    for title in titles:
        try:
            parts = title.split('_')
            if len(parts) == 5:
                date, debit, vendor, amount_str, memo = parts
            elif len(parts) == 4:
                date, debit, vendor, amount_str = parts
                memo = ""
            else:
                raise ValueError(f"要素数が4または5ではありません（{len(parts)}）")

            amount = int(amount_str.replace(',', '').replace('円', ''))

            record = {
                "取引No": "",
                "取引日": date.replace('.', '/'),
                "借方勘定科目": debit,
                "借方金額(円)": amount,
                "貸方勘定科目": "未払金",
                "貸方金額(円)": amount,
                "摘要": vendor,
                "仕訳メモ": memo,
            }
            records.append(record)

        except Exception as e:
            errors.append((title, str(e)))

    return records, errors
