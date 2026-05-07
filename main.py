def menu_zalo():
    cls()
    print(get_banner())
    print(Colorate.Horizontal(Colors.rainbow, "1. Chế độ Treo Ngôn (Màu sắc, Media, TTL)"))
    print(Colorate.Horizontal(Colors.rainbow, "2. Chế độ Treo Tag All (@All Nhây Box)"))
    mode = input("\nChọn (1/2): ")
    
    # --- DỮ LIỆU ĐÃ NẠP SẴN CHO HẢI QUÝ ---
    imei = "c5f107db-982e-4875-92d6-1352876c8433-4c998e5f5ff75020ed6dad16881af41d"
    
    # Cookie đã được chuyển đổi sang định dạng dictionary để Bot hiểu
    cookie = {
        '__zi': '3000.SSZejyD6zOgdh2mtnLQWYQN_RAG01ICFj1.1',
        '__zi-legacy': '3000.SSZejyD6zOgdh2mtnLQWYQN_RAG01ICFj1.1',
        'zlang': 'vn',
        '_ga': 'GA1.2.655939952.1778083101',
        '_gid': 'GA1.2.744731849.1778083101',
        'z_uuid': 'c5f107db-982e-4875-92d6-1352876c8433-4c998e5f5ff75020ed6dad16881af41d'
    }
    
    bot = ZaloBotFull(imei, cookie, 0)
    
    print(Fore.YELLOW + "Đang lấy danh sách nhóm...")
    groups = bot.fetch_groups_list()
    
    if not groups:
        print(Fore.RED + "Lỗi: Không lấy được nhóm. Cookie có thể đã hết hạn hoặc sai!")
        input("Nhấn Enter để quay lại...")
        return

    for i, g in enumerate(groups, 1): 
        print(f"{i}. {g['name']} ({g['id']})")
    
    sel = phan_tich_lua_chon(input("\nChọn nhóm (vd: 1,3): "), len(groups))
    gids = [groups[i-1]['id'] for i in sel]
    
    if mode == '1':
        msg_file = input("File nội dung spam (.txt): ")
        msg_text = "\n".join(doc_file_noi_dung(msg_file))
        delay = float(input("Delay (giây): "))
        colors = phan_tich_lua_chon(input("Màu (1:Đỏ, 2:Cam, 3:Vàng, 4:Xanh, 5:Trắng): "), 5)
        ttl_choice = input("Bật TTL? (Y/N): ").lower()
        ttl = int(float(input("Giây TTL: "))*1000) if ttl_choice == 'y' else None
        
        media_choice = input("Treo Ảnh (Y), Video (N), hay Không (O): ").lower()
        m_type, m_src = "text", ""
        if media_choice == 'y': m_type, m_src = "image", input("Thư mục ảnh: ")
        elif media_choice == 'n': m_type, m_src = "video", input("File URL video: ")

        for gid in gids:
            flag = multiprocessing.Value('b', True)
            multiprocessing.Process(target=bot.run_treo_ngon, args=(gid, msg_text, colors, m_type, m_src, flag, ttl)).start()
    else:
        msg_file = input("File nội dung nhây (.txt): ")
        d_min = float(input("Delay Min: "))
        d_max = float(input("Delay Max: "))
        for gid in gids:
            flag = multiprocessing.Value('b', True)
            multiprocessing.Process(target=bot.run_tag_all, args=(gid, msg_file, flag)).start()
