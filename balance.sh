#!/bin/bash

RAW_DIR="frames"
BALANCED_DIR="balanced_data"
TRAIN_N=500
TEST_N=200

set_count_and_copy() {
  local SRC="$1"       # e.g. frames/train/real
  local DST="$2"       # e.g. balanced_data/train/real
  local COUNT="$3"     # 500 или 200
  local LABEL="$4"     # для сообщений, e.g. "train/real"

  # убедимся, что папка назначения есть
  mkdir -p "$DST"

  # найдём все изображения (рекурсивно)
  local IMAGE_LIST
  IFS=$'\n' read -d '' -r -a IMAGE_LIST < <(find "$SRC" -type f -iname "*.jpg" && printf '\0')

  local TOTAL=${#IMAGE_LIST[@]}
  if [ "$TOTAL" -lt "$COUNT" ]; then
    echo "[ERROR] В $SRC файлов меньше, чем нужно для $LABEL (есть $TOTAL, нужно $COUNT)"
    exit 1
  fi

  # перемешиваем и берём первые COUNT элементов
  mapfile -t SELECTED < <(printf "%s\n" "${IMAGE_LIST[@]}" | shuf -n "$COUNT")

  # копируем, добавляя к имени папку-видео, чтобы избежать коллизий
  for FILE in "${SELECTED[@]}"; do
    VIDEO_DIR=$(basename "$(dirname "$FILE")")
    BASENAME=$(basename "$FILE")
    cp "$FILE" "$DST/${VIDEO_DIR}_${BASENAME}"
  done

  echo "[OK] Скопировано $COUNT файлов → $DST"
}

for SPLIT in train test; do
  for LABEL in real fake; do
    SRC="$RAW_DIR/$SPLIT/$LABEL"
    DST="$BALANCED_DIR/$SPLIT/$LABEL"
    COUNT=$([ "$SPLIT" = "train" ] && echo "$TRAIN_N" || echo "$TEST_N")
    echo "[INFO] Обрабатываю $SPLIT/$LABEL — нужно $COUNT файлов"
    set_count_and_copy "$SRC" "$DST" "$COUNT" "$SPLIT/$LABEL"
  done
done

echo "[DONE] Сбалансированный набор готов в $BALANCED_DIR"