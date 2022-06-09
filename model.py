import mysql.connector

db = mysql.connector.connect (
    host = "localhost",
    user = "root",
    password = "",
    database = "picturefy" 
)

class Model():
    def __init__(self):
        pass

    #memilih splash screen text dari database
    def funnyLine():
        cur = db.cursor()
        cur.execute("""SELECT * FROM funnyline
                        ORDER BY RAND()
                        LIMIT 1;""")
        return cur.fetchone()[1]

    #mengambil data dari table image_tags 
    def get_imagetags():
        cur = db.cursor()
        cur.execute("""SELECT tags.id, image.id, tags.tag_name, image.filename FROM image_tags
                        left JOIN image ON image_tags.image_id = image.id
                        left JOIN tags ON image_tags.tag_id = tags.id 
                        GROUP BY tags.id ORDER BY RAND() limit 12""")
        return cur.fetchall()

    #mengambil gambar sorting tanggal terbaru
    def get_images_newest():
        cur = db.cursor()
        cur.execute("""SELECT tags.id, image.id, tags.tag_name, image.filename, 
                        image.title, image.desc, image.input_date, users.username FROM image_tags
                        left JOIN image ON image_tags.image_id = image.id
                        LEFT JOIN users ON users.id = image.user_id
                        left JOIN tags ON image_tags.tag_id = tags.id order by image.input_date desc""")
        return cur.fetchall()

    #mengambil gambar sorting random
    def get_images_random():
        cur = db.cursor()
        cur.execute("""SELECT tags.id, image.id, tags.tag_name, image.filename, 
                        image.title, image.desc, image.input_date, users.username FROM image_tags
                        left JOIN image ON image_tags.image_id = image.id
                        LEFT JOIN users ON users.id = image.user_id
                        left JOIN tags ON image_tags.tag_id = tags.id order by rand()""")
        return cur.fetchall()

    #mengambil gambar sorting tanggal terlama
    def get_images_oldest():
        cur = db.cursor()
        cur.execute("""SELECT tags.id, image.id, tags.tag_name, image.filename, 
                        image.title, image.desc, image.input_date, users.username FROM image_tags
                        left JOIN image ON image_tags.image_id = image.id
                        LEFT JOIN users ON users.id = image.user_id
                        left JOIN tags ON image_tags.tag_id = tags.id order by image.input_date asc""")
        return cur.fetchall()

    #mengambil gambar secara specific
    def get_images_specific(title):
        cur = db.cursor()
        if("#" in title):
            x = title.replace("#","")            
            cur.execute(f"""SELECT tags.id, image.id, tags.tag_name, image.filename, 
                            image.title, image.desc, image.input_date, users.username FROM image_tags
                            left JOIN image ON image_tags.image_id = image.id
                            left JOIN tags ON image_tags.tag_id = tags.id 
                            LEFT JOIN users ON users.id = image.user_id
                                    WHERE tags.tag_name LIKE "%{x}%"
                                    order by image.input_date desc""")
        elif("@" in title):
            y = title.replace("@","")            
            cur.execute(f"""SELECT tags.id, image.id, tags.tag_name, image.filename, 
                            image.title, image.desc, image.input_date, users.username FROM image_tags
                            left JOIN image ON image_tags.image_id = image.id
                            left JOIN tags ON image_tags.tag_id = tags.id
                            LEFT JOIN users ON users.id = image.user_id 
                                    WHERE users.username LIKE "%{y}%"
                                    order by image.input_date desc""")
        else:
            cur.execute(f"""SELECT tags.id, image.id, tags.tag_name, image.filename, 
                            image.title, image.desc, image.input_date, users.username FROM image_tags
                            left JOIN image ON image_tags.image_id = image.id
                            left JOIN tags ON image_tags.tag_id = tags.id
                            LEFT JOIN users ON users.id = image.user_id 
                                    WHERE image.title LIKE "%{title}%"
                                    order by image.input_date desc""")

        return cur.fetchall()

    def get_user_based_image(uname):
        cur = db.cursor()           
        cur.execute(f"""SELECT tags.id, image.id, tags.tag_name, image.filename, 
                        image.title, image.desc, image.input_date, users.username FROM image_tags
                        left JOIN image ON image_tags.image_id = image.id
                        left JOIN tags ON image_tags.tag_id = tags.id 
                        LEFT JOIN users ON users.id = image.user_id
                                WHERE users.username = "{uname}"
                                order by image.input_date desc""")

        return cur.fetchall()

    def get_tags_based_image(title):
        cur = db.cursor()           
        cur.execute(f"""SELECT tags.id, image.id, tags.tag_name, image.filename, 
                        image.title, image.desc, image.input_date, users.username FROM image_tags
                        left JOIN image ON image_tags.image_id = image.id
                        left JOIN tags ON image_tags.tag_id = tags.id 
                        LEFT JOIN users ON users.id = image.user_id
                                WHERE tags.id = "{title}"
                                order by image.input_date desc""")

        return cur.fetchall()

    def get_id_based_image(title):
        cur = db.cursor()           
        cur.execute(f"""SELECT tags.id, image.id, tags.tag_name, image.filename, 
                        image.title, image.desc, image.input_date, users.username, users.id FROM image_tags
                        left JOIN image ON image_tags.image_id = image.id
                        left JOIN tags ON image_tags.tag_id = tags.id 
                        LEFT JOIN users ON users.id = image.user_id
                                WHERE image.id = "{title}"
                                order by image.input_date desc""")

        return cur.fetchall()

    #mengambil data dari table tags
    def get_tags():
        cur = db.cursor()
        cur.execute("select * from tags")
        return cur.fetchall()
    
    #melakukan register
    def check_username(username):
        cur = db.cursor()
        cur.execute(f"select count(*) from users where username like '%{username}'")
        return cur.fetchall()

    def check_email(email):
        cur = db.cursor()
        cur.execute(f"select count(*) from users where username like '%{email}'")
        return cur.fetchall()

    def registering(username, password, reg_time, isadmin, email):
        cur = db.cursor()
        cur.execute("""INSERT INTO users (`username`, `password`, `reg_time`, `isadmin`, `email`) 
                    VALUES (%s, %s, %s, %s, %s);""",(username, password, reg_time, isadmin, email,))
        db.commit()
        return True

    #mengambil 1 data dari table users
    def loggin_in(self, uname):
        cur = db.cursor()
        cur.execute(f"SELECT * FROM users WHERE username='{uname}'")
        return cur.fetchone()

    ## < aio image process
    def check_tags(tag_name):
        cur = db.cursor()
        cur.execute(f"select COUNT(*) from tags where tag_name LIKE '%{tag_name}%'")
        return cur.fetchone()

    def get_tags_specific(tag_name):
        cur = db.cursor()
        cur.execute(f"select * from tags where tag_name LIKE '%{tag_name}%'")
        return cur.fetchone()

    def get_tags_latest_id():
        cur = db.cursor()
        cur.execute(f"SELECT * FROM tags ORDER BY id desc LIMIT 0, 1")
        return cur.fetchone()

    def get_images_latest_id():
        cur = db.cursor()
        cur.execute(f"SELECT * FROM image ORDER BY id desc LIMIT 0, 1")
        return cur.fetchone()
    ## end aio>
    
    ## < adding an image process
    def add_newTags(id, value):
        cur = db.cursor()
        cur.execute(f"INSERT INTO tags(id, tag_name) VALUES({id}, '{value}')")
        db.commit()

    def add_newImages(id, title, desc, user_id, filename, input_date):
        cur = db.cursor()
        cur.execute("""INSERT INTO `image` (`id`, `title`, `desc`, `user_id`, `filename`, `input_date`) 
                        VALUES (%s,%s,%s,%s,%s,%s)""", (id, title, desc, user_id, filename, input_date,))
        db.commit()

    def add_newImgTgs(image_id, tag_id):
        cur = db.cursor()
        cur.execute("INSERT INTO image_tags (image_id, tag_id) VALUES (%s, %s);", (image_id, tag_id,))
        db.commit()
        return True
    ## end adding an image process >

    ## < delete an image process
    def delete_imageTag(id):
        cur = db.cursor()
        cur.execute(f"DELETE FROM image_tags WHERE image_id={id}")
        db.commit()

    def delete_image(id):
        cur = db.cursor()
        cur.execute(f"DELETE FROM image WHERE id={id}")
        db.commit()
    ## end delete>

    ## < edit an image process
    def edit_newImages(id, title, desc):
        cur = db.cursor()
        cur.execute("UPDATE image SET title=%s, `desc`=%s WHERE id = %s;", (title, desc, id,))
        db.commit()
        return True

    def edit_newImgTgs(image_id, tag_id):
        cur = db.cursor()
        cur.execute("UPDATE image_tags SET tag_id=%s WHERE image_id = %s;", (tag_id, image_id,))
        db.commit()
        return True
    ## end edit>

    ## < get total post
    def count_images():
        cur = db.cursor()
        cur.execute("SELECT COUNT(*) FROM image")
        return cur.fetchone()

    def count_tags():
        cur = db.cursor()
        cur.execute("SELECT COUNT(*) FROM tags")
        return cur.fetchone()

    def count_tags_based_images(title):
        cur = db.cursor()
        cur.execute(f"SELECT COUNT(*) FROM image_tags WHERE tag_id='{title}'")
        return cur.fetchone()     

    def count_user_based_images(title):
        cur = db.cursor()
        cur.execute(f"SELECT COUNT(*) FROM image WHERE user_id='1'='{title}'")
        return cur.fetchone()     

    def count_search_based_images(title):
        cur = db.cursor()

        if("#" in title):
            x = title.replace("#","")            
            cur.execute(f"""SELECT COUNT(tags.id) FROM image_tags
                            left JOIN image ON image_tags.image_id = image.id
                            left JOIN tags ON image_tags.tag_id = tags.id 
                            LEFT JOIN users ON users.id = image.user_id
                                    WHERE tags.tag_name LIKE "%{x}%"
                                    order by image.input_date desc""")
        elif("@" in title):
            y = title.replace("@","")            
            cur.execute(f"""SELECT COUNT(tags.id) FROM image_tags
                            left JOIN image ON image_tags.image_id = image.id
                            left JOIN tags ON image_tags.tag_id = tags.id
                            LEFT JOIN users ON users.id = image.user_id 
                                    WHERE users.username LIKE "%{y}%"
                                    order by image.input_date desc""")
        else:
            cur.execute(f"""SELECT COUNT(tags.id) FROM image_tags
                            left JOIN image ON image_tags.image_id = image.id
                            left JOIN tags ON image_tags.tag_id = tags.id
                            LEFT JOIN users ON users.id = image.user_id 
                                    WHERE image.title LIKE "%{title}%"
                                    order by image.input_date desc""")

        return cur.fetchone()   
    ## end get total post >


#############################################################################################################
#DASHBOARD
#############################################################################################################
    
    def get_user_data():
        cur = db.cursor()
        cur.execute("select * from users")
        return cur.fetchall()

    def sayonara_user(id):
        cur = db.cursor()
        cur.execute(f"DELETE FROM users WHERE id={id}")
        db.commit()

    #mengambil gambar sorting tanggal terbaru
    def get_images_id_order():
        cur = db.cursor()
        cur.execute("""SELECT tags.id, image.id, tags.tag_name, image.filename, 
                        image.title, image.desc, image.input_date, users.username FROM image_tags
                        left JOIN image ON image_tags.image_id = image.id
                        LEFT JOIN users ON users.id = image.user_id
                        left JOIN tags ON image_tags.tag_id = tags.id ORDER BY image.id asc""")
        return cur.fetchall()