name: Build Russian ADS hosts

on:
  schedule:
    - cron: '0 3 * * *'   # ежедневное обновление в 03:00 UTC
  workflow_dispatch:       # запуск вручную

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'

      - name: Install deps
        run: pip install requests

      - name: Build russian-hosts.txt
        run: python build.py

      - name: Commit and push if changed
        run: |
          # Добавляем файл в индекс (в т.ч. если он новый)
          git add russian-hosts.txt

          # Проверяем изменения в индексе
          if git diff --cached --quiet; then
            echo "No changes – nothing to commit."
          else
            git config user.name "github-actions[bot]"
            git config user.email "github-actions[bot]@users.noreply.github.com"
            git commit -m "Update russian-hosts.txt"
            git push
          fi
