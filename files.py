# Modes
# 'r' # open for reading (default)
# 'w' # open for writing, truncating the file first
# 'x' # open for exclusive creation, failing if the file already exists
# 'a' # open for writing, appending to the end of file if it exists
# 'b' # binary mode
# 't' # text mode (default)
# '+' # open for updating (reading and writing)

# with statement closes the file automatically!
with open("demo.txt", mode="a+") as f:
    f.write("Testing this!\n")
    # If another handle/process will read the file,
    # flush is mandatory (seek alone only affects your handle/same open file object (the same stream)
    f.flush()
    # Move the cursor back to the beginning of the file
    f.seek(0)

    # file_content = f.read()
    # print(file_content)

    # f.seek(0)
    # readlines returns a list of lines that can be processed individually
    # file_content = f.readlines()
    # print(file_content)
    # f.close()

    # for line in file_content:
    #     print(line.strip())

    line = f.readline()
    while line:
        print(line)
        line = f.readline()
print("Done!")
