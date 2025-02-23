from asro_preprocessing.preprocessing import AsroPreprocessing

# Inisialisasi class
preprocessor = AsroPreprocessing()

# Jalankan preprocessing pada file input
df = preprocessor.preprocess(
    input_path="data/comments.xlsx",             # Path ke file Excel input
    text_column="comment",                       # Kolom teks yang akan diproses
    channel_title_column="channel_title",        # Kolom yang berisi judul channel
    output_path="output/processed_comments.xlsx" # Path untuk menyimpan output
)

# Tampilkan hasil
print(df.head())
