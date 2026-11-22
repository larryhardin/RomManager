#!/usr/bin/env bash

start_rom_db() {
    local xml_file="${1:-./mame0288.xml}"
    if [[ ! -f "$xml_file" ]]; then
        echo "Error: $xml_file not found."
        return 1
    fi

    # Stop any existing instance first
    stop_rom_db 2>/dev/null

    echo "Loading $xml_file into resident memory..."

    coproc ROM_DB {
        awk -v xml="$xml_file" '
        BEGIN {
            FS = "\""
            while ((getline line < xml) > 0) {
                lines++
                if (lines % 1000000 == 0) {
                    printf("  ...parsed %dM lines\n", lines / 1000000) > "/dev/stderr"
                }
                if (index(line, "<machine name=\"")) {
                    split(line, a, "\"")
                    cur_name = a[2]
                    cur_desc = ""
                } else if (cur_name != "" && cur_desc == "" && index(line, "<description>")) {
                    sub(/.*<description>/, "", line)
                    sub(/<\/description>.*/, "", line)
                    cur_desc = line
                } else if (cur_name != "" && index(line, "crc=\"")) {
                    match(line, /crc="[0-9a-fA-F]+"/)
                    rom_crc = tolower(substr(line, RSTART + 5, RLENGTH - 6))
                    if (!(rom_crc in map)) {
                        map[rom_crc] = cur_name "|" cur_desc
                    }
                }
            }
            close(xml)
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

    # Read from index [0] (stdout of coproc)
    local status
    read -r status <&"${ROM_DB[0]}"
    if [[ "$status" == "READY" ]]; then
        echo "MAME database resident and ready! Use: checkrom <file.zip | crc32>"
    fi
}

checkrom() {
    local target="$1"
    if [[ -z "$ROM_DB_PID" ]]; then
        echo "Database not running. Run: start_rom_db /path/to/mame0288.xml"
        return 1
    fi

    local crc=""
    local shortname=""

    if [[ -f "$target" ]]; then
        local filename=$(basename "$target")
        shortname="${filename%.zip}"
        crc=$(unzip -v "$target" 2>/dev/null | awk '/^[[:space:]]*[0-9]+/ {print tolower($7); exit}')
    else
        crc=$(echo "$target" | tr '[:upper:]' '[:lower:]')
    fi

    if [[ -z "$crc" ]]; then
        echo "[ERROR] Could not extract CRC from $target"
        return 1
    fi

    # Write to index [1] (stdin of coproc) and read from index [0] (stdout)
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
        kill "$ROM_DB_PID" 2>/dev/null
        unset ROM_DB_PID
        echo "Resident MAME database stopped."
    fi
}