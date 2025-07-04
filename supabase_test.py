from supabase_utils.test_connection import test_connection

if __name__ == "__main__":
    result = test_connection()
    if result:
        print("Supabase接続テスト：成功！")
    else:
        print("Supabase接続テスト：失敗！")
