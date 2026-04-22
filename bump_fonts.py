import os
import glob
import re

def bump_fonts():
    views_dir = os.path.join(os.path.dirname(__file__), 'views')
    py_files = glob.glob(os.path.join(views_dir, '*.py'))
    
    # Also include login_window.py (it's in views)
    
    for fp in py_files:
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
            
        def replacer(match):
            size = int(match.group(1))
            new_size = size + 2  # Increase by 2px
            return f"font-size: {new_size}px"
            
        # Tăng font size
        new_content = re.sub(r'font-size:\s*(\d+)px', replacer, content)
        
        # Sửa một số style input field/button cho to hơn tương ứng
        new_content = re.sub(r'min-height:\s*36px', 'min-height: 42px', new_content)
        new_content = re.sub(r'min-height:\s*32px', 'min-height: 38px', new_content)
        new_content = re.sub(r'padding:\s*8px\s*14px', 'padding: 10px 16px', new_content)
        new_content = re.sub(r'padding:\s*10px\s*12px', 'padding: 14px 16px', new_content)
        new_content = re.sub(r'padding:\s*7px\s*10px', 'padding: 10px 14px', new_content)
        
        if content != new_content:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated sizes in {os.path.basename(fp)}")

if __name__ == '__main__':
    bump_fonts()
    print("DONE BUMPING FONTS")
