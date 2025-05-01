def transform_notes(titles):
    records = []
    errors = []

    for title in titles:
        try:
            date, debit, vendor, amount_str, memo = title.split('_')
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

    if errors:
        print("\n⚠️ 以下のノート題名は形式エラーのためスキップされました：")
        for i, (title, err_msg) in enumerate(errors, 1):
            print(f"{i:>2}. '{title}' → {err_msg}")

    print(f"\n✅ 正常処理数：{len(records)} 件")
    print(f"❌ スキップ数：{len(errors)} 件")

    return records
