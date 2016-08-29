#!/bin/bash
mkdir tests/data/source/Dir{A..C}
mkdir tests/data/source/Dir{A..C}/SubDir_{a..b}
touch tests/data/source/Dir{A..C}/file{1..3}
touch tests/data/source/Dir{A..C}/SubDir_{a..b}/f{1..3}
