# Litracker 

`PBP A - Kelompok A01`

### Anggota 👨‍💻👩‍💻:
1. Anindya Maulida Widyatmoko - 2206082915
2. Henry Soedibjo - 2206827762
3. Muhammad Fawwaz Arshad Said - 2206082511
4. Haffie Noorcahyo - 2206081515
5. Muhammad Daffa Grahito Triharsanto - 2206820075

## Cerita Aplikasi dan Manfaat 💻
**Litracker** adalah sebuah platform pendidikan digital yang berfokus pada peningkatan literasi siswa. Dilengkapi dengan fitur-fitur seperti autentikasi, rekomendasi buku yang disesuaikan, buku favorit, ulasan buku, dan pencarian buku yang canggih, Litracker bertujuan untuk membantu siswa menjelajahi, memahami, dan meningkatkan kemampuan literasi mereka secara interaktif dan mendidik. Dengan Litracker, pengguna dapat dengan mudah menemukan buku-buku sesuai minat mereka, memberikan ulasan, serta melacak dan meningkatkan kemampuan literasi mereka. 

Manfaat besar dari platform ini adalah dalam meningkatkan minat literasi di Indonesia. Fitur rekomendasi buku yang disesuaikan dan pencarian buku yang canggih memudahkan akses pengguna terhadap buku-buku yang menarik minat mereka, merangsang minat membaca siswa, membantu mereka menjelajahi dunia literasi, dan memajukan kemampuan literasi. Selain itu, melalui fitur ulasan buku, Litracker juga menciptakan komunitas literasi yang potensial untuk memengaruhi masyarakat secara lebih luas, mendekatkan mereka pada dunia membaca, dan memperkuat budaya literasi di Indonesia. Dengan demikian, Litracker bukan hanya alat pendidikan, melainkan juga pendorong penting dalam memperkuat minat literasi dan budaya membaca di Indonesia.

## Daftar Modul 💡
**Litracker menawarkan beberapa modul yang tersedia, antara lain:**

<details><summary>1. Buku</summary>
Fitur “Buku” akan menampilkan buku-buku dan bisa diakses oleh user, guest, dan admin. Perbedaan pengaksesan admin, user, dan guest yaitu:

a. Create (Tambah buku)
Pada dashboard, admin dapat menambahkan buku yang akan ditampilkan di laman rekomendasi buku.

b. Read (Baca buku dan lihat detail buku)
Buku yang telah ditambahkan admin bisa diakses oleh user pada detail buku yang melampirkan deskripsi, author, dan lain-lain. Pengunjung juga dapat melihat detail buku walaupun akses lanjutan terbatas.

c. Delete (Hapus buku)
Admin dapat menghapus buku jika dirasa kurang relevan atau terdapat suatu kesalahan.

d. Update (Mengedit informasi buku)
Admin dapat melakukan pengeditan pada buku yang telah dibuat. Hal ini juga berdampak kepada user dan pengunjung pada mode read.
</details>

<details><summary>2. Buku Favorit (Data Favorit buku tiap user)</summary>
"Buku Favorit" adalah sebuah komponen yang memungkinkan pengguna untuk mengelola buku-buku yang mereka tandai sebagai favorit. Dalam operasi "Create," pengguna dapat menambahkan buku baru ke daftar favorit mereka dengan mengidentifikasi buku tersebut berdasarkan atribut seperti ID buku. Dalam operasi "Read," pengguna dapat melihat daftar buku favorit mereka. Dalam operasi "Update," pengguna dapat mengedit atau memperbarui informasi buku favorit yang telah ada dalam daftar mereka. Akhirnya, dalam operasi "Delete," pengguna dapat menghapus buku dari daftar favorit mereka jika mereka tidak lagi ingin menyimpannya. Model ini memastikan pengguna memiliki kendali penuh atas buku-buku yang mereka pilih sebagai favorit, meningkatkan pengalaman personalisasi dan interaksi dengan platform pendidikan literasi.
</details>

<details><summary>3. Review Buku (review setiap buku dari user)</summary>
Review Buku dimana pengguna dapat memberikan ulasan dan pandangan pribadi mereka terhadap buku yang telah mereka baca. 

a. Create :
Ketika pengguna ingin membuat ulasan baru untuk suatu buku yang telah mereka baca. Pengguna dapat memberikan peringkat dengan jumlah bintang, menambahkan judul ulasan, dan menulis ulasan mereka sendiri tentang buku tersebut. Proses ini memungkinkan pengguna untuk berbagi pengalaman dan pandangan mereka dengan pengguna lain.

b. Update :
Ketika pengguna ingin mengedit ulasan yang telah mereka buat sebelumnya. Pengguna dapat memperbarui peringkat bintang, mengubah judul ulasan, atau memperbarui konten ulasan sesuai dengan perubahan pendapat mereka tentang buku tersebut. Ini memberikan fleksibilitas kepada pengguna untuk memperbarui ulasan mereka seiring berjalannya waktu atau setelah membaca buku lebih lanjut.

c. Edit :
Ketika pengguna ingin mengoreksi atau memperbaiki informasi yang mereka masukkan dalam ulasan. Pengguna dapat memperbaiki tata bahasa, struktur kalimat, atau kesalahan pengetikan yang mungkin terjadi saat menulis ulasan.

d. Read:
Pengguna dapat membaca ulasan review buku pengguna lain untuk mendapatkan rekomendasi mendalam terkait kecocokan dengan buku yang sesuai dengan preferensi mereka.

e. Delete :
Ketika pengguna ingin menghapus ulasan yang mereka buat sebelumnya. Pengguna dapat memilih untuk menghapus ulasan jika mereka tidak ingin ulasan tersebut tersedia untuk publik atau jika mereka ingin menarik ulasan yang tidak lagi mewakili pendapat mereka.
</details>

<details><summary>4. Reading History (buku yang telah dibaca user)</summary>
Reading History akan mencatat buku yang telah dibaca oleh pengguna. Penjelasan secara implementasi CRUDnya seperti dibawah ini:

a. Create (Membuat Data Riwayat Bacaan):
Ketika seorang pengguna menyelesaikan membaca sebuah buku, maka akan dibuat catatan baru dalam model Reading History.
Informasi seperti ID pengguna, ID buku yang telah dibaca, tanggal selesai membaca, dan mungkin sejauh mana kemajuan yang telah dicapai oleh pengguna (misalnya, halaman terakhir yang dibaca) akan disimpan.

b. Read (Membaca Data Riwayat Bacaan):
Pengguna dapat membaca riwayat bacaan mereka dengan mudah untuk melihat buku mana yang telah mereka baca sebelumnya. Mereka dapat melihat informasi seperti judul buku, penulis, tanggal selesai membaca, dan kemajuan membaca.

c. Update (Memperbarui Data Riwayat Bacaan):
Pengguna dapat memperbarui data riwayat bacaan mereka jika mereka ingin menambahkan informasi tambahan, seperti tanggal selesai membaca atau kemajuan membaca yang lebih baru.
Misalnya, jika pengguna ingin menandai ulang buku sebagai "Dibaca Kembali" atau "Selesai," mereka dapat memperbarui catatan ini.

d. Delete (Menghapus Data Riwayat Bacaan):
Pengguna juga harus memiliki opsi untuk menghapus buku dari riwayat bacaan mereka jika mereka ingin menghapus buku tertentu dari catatan mereka.
</details>

<details><summary>5. Upvote Buku (User dapat memberikan vote ke buku yang mereka sukai)</summary>
Upvote buku akan memberikan status populer pada buku. Penjelasan secara implementasi CRUD sebagai berikut:

a. Create (Menambahkan Buku ke List Buku yang Diupvote pada Dashboard)
Pengguna dapat menekan tombol upvote pada buku yang dinilai menarik. Pada dashboard akan ditampilkan buku yang diupvote.

b. Read (Melihat Buku yang Diupvote)
Pada laman dashboard, pengguna dapat melihat buku yang mereka upvote.

c. Update (Memperbarui Peringkat Buku)
Buku akan disorting berdasarkan peringkat. Dalam hal ini, peringkat diambil dari total banyak vote yang diperoleh. Peringkat buku-buku akan diupdate seiring bertambah atau berkurangnya upvote.

d. Delete (Menghapus Buku dari Daftar Upvote)
Pengguna dapat undo upvote buku sehingga buku akan keluar dari daftar list upvote book mereka.
</details>


## Fitur utama Litracker

<details><summary>1. Authentication</summary>
Fitur Authentication dalam Litracker adalah proses di mana pengguna dapat masuk ke platform dengan akun mereka atau membuat akun baru. Hal ini bertujuan untuk menjaga keamanan informasi pengguna dan memberikan akses yang aman ke fitur-fitur platform. Fitur authentication ini terdiri dari 2, yaitu login dan register dengan melibatkan penggunaan kombinasi username dan password yang unik. 
</details>

<details><summary>2. Navbar</summary>

a. Search Book
Fitur "Search Book" memungkinkan pengguna untuk dengan mudah menemukan buku-buku berdasarkan berbagai kriteria seperti judul, penulis, genre, atau kata kunci lainnya. Dengan fitur ini, pengguna dapat mengeksplorasi dan menemukan buku-buku yang sesuai dengan preferensi mereka dengan cepat dan efisien.

b. Favorite Book (icon love)
Fitur "Favorite Book" adalah cara bagi pengguna untuk menandai dan mengelola buku-buku yang mereka sukai secara khusus. Dengan mengklik ikon hati (icon love) di buku-buku yang menarik perhatian mereka, pengguna dapat menambahkan buku-buku ini ke daftar "Favorite Book" mereka. Ini memungkinkan pengguna untuk dengan cepat mengakses dan mengingat buku-buku yang paling mereka sukai. Selain itu, fitur ini membantu pengguna dalam menyusun dan memelihara koleksi buku favorit mereka untuk referensi dan pembacaan selanjutnya.
</details>

<details><summary>3. Rekomendasi Buku - Buku populer berdasarkan rank authors (landing page)</summary>
Fitur Rekomendasi Buku adalah salah satu fitur dalam Litracker yang dirancang untuk membantu pengguna menemukan buku-buku yang sesuai dengan minat mereka. Pada Landing Page, Rekomendasi Buku akan menjadi halaman utama yang muncul ketika pengguna masuk ke akun mereka. Halaman ini akan menampilkan daftar buku-buku populer yang disusun berdasarkan peringkat penulis. Pengguna akan melihat penulis-penulis terkenal dan buku-buku mereka yang sangat direkomendasikan oleh komunitas agar dapat dimasukkan ke dalam daftar membaca pengguna. Sistem peringkat ini didasarkan pada ulasan dan peringkat yang diberikan oleh pengguna Litracker. 
</details>

<details><summary>4. Review Buku</summary>
Fitur Review Buku memungkinkan pengguna untuk berbagi pandangan mereka tentang buku-buku yang telah mereka baca. Ini membantu pengguna lain dalam mengevaluasi buku sebelum memutuskan untuk membacanya. Halaman Review Buku adalah halaman khusus yang memungkinkan pengguna membuat ulasan dari suatu buku. Saat menulis ulasan, pengguna dapat memberikan peringkat berdasarkan jumlah bintang, memberikan judul ulasan, dan menulis ulasan mereka sendiri. Mereka dapat menyatakan opini mereka tentang plot, karakter, gaya penulisan, dan aspek-aspek lain dari buku tersebut.
</details>

<details><summary>5. Upvote Buku</summary>
Fitur Upvote Buku memungkinkan pengguna untuk mendukung konten buku yang menarik minat bacanya. Dalam hal ini, ketika pengguna melakukan upvote, peringkat buku terpengaruh sehingga akan terupdate daftar buku yang ditampilkan. 
</details>

<details><summary>6. Dashboard User</summary>

a. Favorite book
Fitur "Favorite Book" pada Litracker membantu pengguna untuk lebih baik mengelola minat literasi mereka, menyediakan akses cepat ke buku-buku yang mereka sukai. Fitur ini memungkinkan pengguna untuk menyimpan dan mengatur buku-buku yang mereka favoritkan atau yang ingin mereka baca nanti.

b. Profile
Fitur ini Pengguna dapat mengelola dan memperbarui informasi pribadi mereka, seperti nama, alamat email, foto profil.

c. Upvote History
Pengguna mendapat pembaruan terhadap aktivitas upvote yang ia lakukan. Dalam hal ini, pengguna bisa mengecek kekeliruan maupun mengupdate pembaruan yang terjadi.

d. Reading History
Pengguna dapat melihhat buku yang terakhir kali dibaca. Dalam hal ini, delete mengizinkan pengguna untuk menyembunyikan hasil bacaan jika diperlukan.
</details>


## Sumber dataset katalog buku
https://www.kaggle.com/datasets/sp1thas/book-depository-dataset/ 


## Role dan Peran Pengguna

<details><summary>1. Admin</summary>
Admin memiliki kontrol penuh atas Litracker yang dapat  bisa mengubah, memperbarui, dan mengelola data. Admin menjaga keamanan dan kinerja platform ini. Selain itu, admin juga bisa memberikan izin akses kepada pengguna untuk mengakses fitur-fitur yang ada di Litracker seperti Review buku, favorite book, dan fitur-fitur lain yang dapat digunakan oleh Login user.  
</details>

<details><summary>2. Guest user</summary>
Guest user adalah pengunjung yang mengunjungi Litracker tanpa melakukan otentikasi atau login. Guest user dapat melakukan penelusuran dan menggunakan fitur Litracker seperti melihat info, mencari buku, baca rekomendasi, dan lihat ulasan. Namun, tidak memiliki akses untuk memberi ulasan atau tandai buku sebagai favorit tanpa login.
</details>

<details><summary>3. Logged in user</summary>
Pengguna yang sudah login bisa lakukan lebih banyak hal. Mereka bisa unduh dataset, beri penilaian, tulis ulasan, dan lain-lain. Pengguna yang sudah login juga bisa akses fitur tambahan sesuai dengan aturan platform. Mereka juga bisa ikuti update dataset, bagikan dataset, atau simpan dataset favorit.
</details>


## Diagram Web Flow Akun

<details><summary>Memilih tipe akun saat masuk pertama kali</summary>
Pengunjung pertama kali akan memasuki landing page yang berisi rekomendasi buku. Dalam hal ini, ketika pengunjung melakukan aksi login, pengunjung akan dialihkan ke tipe masing-masing akun.
</details>

![Tipe Akun](/Account%20Type%20Decision.png)

<details><summary>Information Architecture Guest</summary>
Pengunjung memiliki akses yang sangat terbatas. Pengunjung yang melakukan suatu aksi pada laman yang tidak mendapat izin akses akan dialihkan ke laman login.
</details>

![IA Guest](/Information%20Architecture%20Guest.png) 

<details><summary>Information Architecture User</summary>
Pengunjung yang sudah login bisa menikmati akses Litracker. Adapun aksi CRUD yang bisa diterima antara lain:
</details>

![IA User](/Information%20Architecture%20User.png)

<details><summary>Information Architecture Admin</summary>
Akun admin difokuskan ke dalam manajemen akun sehingga akses dashboard terhadap manajemen akun user dan kumpulan buku akan diizinkan.
</details>

![IA Admin](/Information%20Architecture%20Admin.png) 
