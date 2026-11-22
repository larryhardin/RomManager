#!/usr/bin/env bash

start_rom_db() {
    local xml_file="${1:-./mame0288.xml}"
    local db_file="${xml_file%.xml}.db"
    local cores
    cores=$(nproc 2>/dev/null || echo 56)

    if [[ ! -f "$xml_file" && ! -f "$db_file" ]]; then
        echo "Error: Neither $xml_file nor $db_file found."
        return 1
    fi

    # 1. Parallel multi-core build of mame0288.db across all CPUs
    if [[ ! -f "$db_file" || "$xml_file" -nt "$db_file" ]]; then
        local build_start=$SECONDS
        echo "[$(date '+%H:%M:%S')] Start building $db_file across $cores CPU cores..."
        local tmp_dir
        tmp_dir=$(mktemp -d)

        local total_bytes chunk_bytes
        total_bytes=$(stat -c%s "$xml_file")
        chunk_bytes=$(( total_bytes / cores + 1 ))

        split -C "$chunk_bytes" --filter='
            awk -F"\"" '\''
            /<machine name=/ { cur_name = $2; cur_desc = ""; next }
            cur_name != "" && cur_desc == "" && /<description>/ {
                sub(/.*<description>/, "", $0)
                sub(/<\/description>.*/, "", $0)
                cur_desc = $0
                next
            }
            cur_name != "" && /crc="/ {
                for (i=1; i<NF; i++) {
                    if ($i ~ /crc=$/) {
                        print tolower($(i+1)) "|" cur_name "|" cur_desc
                        break
                    }
                }
            }'\'' > "'"$tmp_dir"'/$FILE.part"
        ' "$xml_file" chunk_

        LC_ALL=C sort -t'|' -k1,1 -u --parallel="$cores" -S 16G "$tmp_dir"/*.part > "$db_file"
        rm -rf "$tmp_dir"

        local build_elapsed=$(( SECONDS - build_start ))
        echo "[$(date '+%H:%M:%S')] End building $db_file ($(wc -l < "$db_file") unique CRCs) in ${build_elapsed}s."
    fi

    # 2. Clean up any existing coproc cleanly before starting
    stop_rom_db

    local load_start=$SECONDS
    echo "[$(date '+%H:%M:%S')] Start loading $db_file into resident memory..."
    coproc ROM_DB {
        awk -F'|' -v db="$db_file" '
        BEGIN {
            while ((getline line < db) > 0) {
                idx = index(line, "|")
                crc = substr(line, 1, idx - 1)
                map[crc] = substr(line, idx + 1)
            }
            close(db)
            print "READY"
            fflush()
        }
        {
            crc = tolower($1)
            if (crc in map) {
                print map[crc]
            } else {
                print "NOT_FOUND"
            }
            fflush()
        }'
    }

    local status
    read -r status <&"${ROM_DB[0]}"
    if [[ "$status" == "READY" ]]; then
        local load_elapsed=$(( SECONDS - load_start ))
        echo "[$(date '+%H:%M:%S')] End loading resident MAME DB in ${load_elapsed}s. Ready! Run: checkrom <file.zip | crc32>"
    fi
}

checkrom() {
    local target="$1"
    if [[ -z "$ROM_DB_PID" ]]; then
        echo "Database not running. Run: start_rom_db ./mame0288.xml"
        return 1
    fi

    local crc=""
    local shortname=""

    if [[ -f "$target" ]]; then
        local filename
        filename=$(basename "$target")
        shortname="${filename%.zip}"
        crc=$(unzip -v "$target" 2>/dev/null | awk '/^[[:space:]]*[0-9]+/ {print tolower($7); exit}')
    else
        crc=$(echo "$target" | tr '[:upper:]' '[:lower:]')
    fi

    if [[ -z "$crc" ]]; then
        echo "[ERROR] Could not extract CRC from $target"
        return 1
    fi

    printf "%s\n" "$crc" >&"${ROM_DB[1]}"
    local result
    read -r result <&"${ROM_DB[0]}"

    if [[ "$result" == "NOT_FOUND" ]]; then
        echo "[UNKNOWN] $target (CRC $crc not in MAME 0.288)"
    else
        local match_name="${result%%|*}"
        local match_desc="${result#*|}"
        if [[ -n "$shortname" && "$match_name" != "$shortname" ]]; then
            echo "[RENAMED] $shortname.zip  -->  $match_name.zip ($match_desc)"
        else
            echo "[MATCH]   $match_name.zip ($match_desc)"
        fi
    fi
}

stop_rom_db() {
    if [[ -n "$ROM_DB_PID" ]]; then
        local fd_in="${ROM_DB[1]}"
        local fd_out="${ROM_DB[0]}"
        [[ -n "$fd_in" ]] && eval "exec ${fd_in}>&-" 2>/dev/null
        [[ -n "$fd_out" ]] && eval "exec ${fd_out}<&-" 2>/dev/null
        kill -9 "$ROM_DB_PID" 2>/dev/null
        wait "$ROM_DB_PID" 2>/dev/null
        unset ROM_DB ROM_DB_PID
    fi
}