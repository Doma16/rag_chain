import kagglehub

path1 = kagglehub.dataset_download("crawford/20-newsgroups")
path2 = kagglehub.dataset_download("rtatman/blog-authorship-corpus")
path3 = kagglehub.dataset_download("mateibejan/15000-gutenberg-books")

print(f"Downloaded datasets to: {path1}, {path2} and {path3}")