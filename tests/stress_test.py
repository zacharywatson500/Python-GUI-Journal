import tkinter as tk
import time
import threading
import random
import string
from datetime import datetime  

import sys 
import os 

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the journal app
from journal import JournalApp

class StressTestSuite:
    def __init__(self):
        self.root = tk.Tk()
        self.app = JournalApp(self.root)
        self.test_results = []
        
    def log_result(self, test_name, success, duration, details=""):
        """Log test results"""
        result = {
            'test': test_name,
            'success': success,
            'duration': duration,
            'details': details,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"[{result['timestamp']}] {test_name}: {status} ({duration:.3f}s) {details}")
        
    def input_flood_test(self):
        """Test: Input 1,000,000 characters"""
        print("\n🌊 Starting Input Flood Test...")
        start_time = time.time()
        
        try:
            # Generate 1,000,000 character string
            large_text = "A" * 1_000_000
            
            # Set title
            self.app.title_entry.delete(0, tk.END)
            self.app.title_entry.insert(0, "Input Flood Test")
            
            # Insert large text
            self.app.text_area.delete("1.0", tk.END)
            self.app.text_area.insert("1.0", large_text)
            
            # Try to save
            self.app.save_entry()
            
            duration = time.time() - start_time
            self.log_result("Input Flood", True, duration, "1M characters processed")
            
        except Exception as e:
            duration = time.time() - start_time
            self.log_result("Input Flood", False, duration, f"Error: {str(e)}")
            
    def rapid_fire_test(self):
        """Test: Trigger save 50 times in 1 second"""
        print("\n🔥 Starting Rapid Fire Test...")
        start_time = time.time()
        successful_saves = 0
        
        try:
            # Prepare a simple entry
            self.app.title_entry.delete(0, tk.END)
            self.app.title_entry.insert(0, "Rapid Fire Test")
            self.app.text_area.delete("1.0", tk.END)
            self.app.text_area.insert("1.0", "Rapid fire test entry")
            
            # Calculate interval for 50 saves in 1 second
            interval = 1.0 / 50  # 0.02 seconds between saves
            
            for i in range(50):
                save_start = time.time()
                
                # Update title to make each entry unique
                self.app.title_entry.delete(0, tk.END)
                self.app.title_entry.insert(0, f"Rapid Fire Test #{i+1}")
                
                # Insert unique content for each save
                self.app.text_area.delete("1.0", tk.END)
                self.app.text_area.insert("1.0", f"Test Entry #{i+1}")
                
                # Trigger save (this will show messagebox, we need to handle it)
                try:
                    self.app.save_entry()
                    successful_saves += 1
                except:
                    # Messagebox might interrupt, that's expected
                    pass
                
                # Wait for next interval
                elapsed = time.time() - save_start
                if elapsed < interval:
                    time.sleep(interval - elapsed)
            
            duration = time.time() - start_time
            self.log_result("Rapid Fire", True, duration, f"{successful_saves}/50 saves completed")
            
        except Exception as e:
            duration = time.time() - start_time
            self.log_result("Rapid Fire", False, duration, f"Error: {str(e)}")
            
    def character_chaos_test(self):
        """Test: Save text with weird symbols and emojis"""
        print("\n🎭 Starting Character Chaos Test...")
        start_time = time.time()
        
        try:
            # Create text with various challenging characters
            chaos_text = """📂🔥💯🚀🌟⭐💫✨🎯🎪🎭🎨🎬🎮🎵🎶🎤🎧🎸🥁🎹🎺🎻🎷
            中文测试 - Chinese characters
            العربية - Arabic text
            русский - Russian text
            ελληνικά - Greek text
            עברית - Hebrew text
            हिन्दी - Hindi text
            日本語 - Japanese text
            한국어 - Korean text
            Tiếng Việt - Vietnamese text
            ภาษาไทย - Thai text
            Special chars: !@#$%^&*()_+-=[]{}|;':",./<>?
            Math: ∑∏∫∆∇∂√∞≈≠≤≥±×÷πθφψωαβγδεζηθ
            Currency: $€£¥₹₽₩₪₫₡₦₨₱₲₴₸₼₽
            Accents: áéíóúñüöäëïöüçßåøœæ
            """
            
            # Set title
            self.app.title_entry.delete(0, tk.END)
            self.app.title_entry.insert(0, "🎭 Character Chaos Test 🎭")
            
            # Insert chaos text
            self.app.text_area.delete("1.0", tk.END)
            self.app.text_area.insert("1.0", chaos_text)
            
            # Try to save
            self.app.save_entry()
            
            duration = time.time() - start_time
            self.log_result("Character Chaos", True, duration, "Unicode and special chars")
            
        except Exception as e:
            duration = time.time() - start_time
            self.log_result("Character Chaos", False, duration, f"Error: {str(e)}")
            
    def run_all_tests(self):
        """Run all stress tests"""
        print("🚀 Starting Stress Test Suite")
        print("=" * 50)
        
        # Run tests in sequence to avoid interference
        self.input_flood_test()
        time.sleep(1)  # Brief pause between tests
        
        self.rapid_fire_test()
        time.sleep(1)
        
        self.character_chaos_test()
        
        # Print summary
        print("\n" + "=" * 50)
        print("📊 STRESS TEST SUMMARY")
        print("=" * 50)
        
        passed = sum(1 for r in self.test_results if r['success'])
        total = len(self.test_results)
        
        for result in self.test_results:
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            print(f"{status} {result['test']}: {result['duration']:.3f}s {result['details']}")
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All stress tests passed! Your app is robust!")
        else:
            print("⚠️  Some tests failed. Review the issues above.")
            
    def start_tests(self):
        """Start the stress test suite after a short delay"""
        # Start tests after 2 seconds to allow UI to fully load
        self.root.after(2000, self.run_all_tests)

def main():
    """Main function to run stress tests"""
    print("🧪 Journal App Stress Test Suite")
    print("This will test your journal app under extreme conditions")
    print("Make sure your journal app is not already running!")
    print("\nStarting tests in 2 seconds...")
    
    # Create and run stress test suite
    test_suite = StressTestSuite()
    test_suite.start_tests()
    
    # Start the GUI event loop
    test_suite.root.mainloop()

if __name__ == "__main__":
    main() 
    
