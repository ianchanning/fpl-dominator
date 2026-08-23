This gameweek I took the screenshots on my phone

I then got Nyx to process them in the mobile app and downloaded the CSV files on the laptop.

They come as txt files so you need to rename them:

```sh
# My guess
for 'gw14/*.txt' do mv {%f}.txt {%f}.csv; done

# Actual
for f in gw14/*.txt; do mv "$f" "${f%.txt}.csv"; done


# for file in glob; do ...; done
for f in gw14/*.txt; do mv "$f" "${f%}.csv"; done

# re-write from memory using `file`
for file in gw14/*.txt; do mv "${file}" "${file%.txt}.csv"; done
```
