import unittest
from simple_util.id_generator import SnowflakeIDGenerator

class TestSnowflakeIDGenerator(unittest.TestCase):
    def test_generate_unique_ids(self):
        id_generator = SnowflakeIDGenerator(machine_id=1, datacenter_id=1)
        generated_ids = set()
        
        for _ in range(100000):
            new_id = id_generator.generate_id()
            # 检查生成的ID是否已经存在
            self.assertNotIn(new_id, generated_ids, f"Duplicate ID found: {new_id}")
            generated_ids.add(new_id)
            # print(new_id)

if __name__ == "__main__":
    unittest.main()