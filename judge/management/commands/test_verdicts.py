from django.core.management.base import BaseCommand
from judge.views import run_code_util
from pathlib import Path
import uuid
from django.conf import settings
import re

def normalize(text):
    return re.sub(r'\s+', ' ', text.strip())

AC_OUTPUT = "12"
INPUT = "5\n7"

accepted_codes = {
    'python': "a=int(input())\nb=int(input())\nprint(a+b)",
    'c': "#include <stdio.h>\nint main(){int a,b;scanf(\"%d %d\",&a,&b);printf(\"%d\\n\",a+b);return 0;}",
    'cpp': "#include<iostream>\nusing namespace std;\nint main(){int a,b;cin>>a>>b;cout<<a+b<<endl;return 0;}",
    'java': "import java.util.*;public class Main{public static void main(String[] args){Scanner sc=new Scanner(System.in);int a=sc.nextInt(),b=sc.nextInt();System.out.println(a+b);}}"
}

verdict_cases = {
    'Accepted': accepted_codes,
    
    'Wrong Answer': {
        'python': "a=int(input())\nb=int(input())\nprint(a-b)",
        'c': "#include <stdio.h>\nint main(){int a,b;scanf(\"%d %d\",&a,&b);printf(\"%d\\n\",a-b);return 0;}",
        'cpp': "#include<iostream>\nusing namespace std;\nint main(){int a,b;cin>>a>>b;cout<<a-b<<endl;return 0;}",
        'java': "import java.util.*;public class Main{public static void main(String[] args){Scanner sc=new Scanner(System.in);int a=sc.nextInt(),b=sc.nextInt();System.out.println(a-b);}}"
    },

    'Time Limit Exceeded': {
        'python': "for _ in range(10**9): pass\na=int(input())\nb=int(input())\nprint(a+b)",
        'c': "#include <stdio.h>\nint main(){for(long long i=0;i<1e10;i++);int a,b;scanf(\"%d %d\",&a,&b);printf(\"%d\\n\",a+b);return 0;}",
        'cpp': "#include<iostream>\nusing namespace std;\nint main(){for(long long i=0;i<1e10;i++);int a,b;cin>>a>>b;cout<<a+b<<endl;return 0;}",
        'java': "import java.util.*;public class Main{public static void main(String[] args){for(long i=0;i<1e10;i++);Scanner sc=new Scanner(System.in);int a=sc.nextInt(),b=sc.nextInt();System.out.println(a+b);}}"
    },

    'Runtime Error': {
        'python': "a=int(input())\nb=int(input())\nprint(5//0)\nprint(a+b)",
        'c': "#include <stdio.h>\nint main(){int a,b;scanf(\"%d %d\",&a,&b);int x=5/0;printf(\"%d\\n\",a+b);return 0;}",
        'cpp': "#include<iostream>\nusing namespace std;\nint main(){int a,b;cin>>a>>b;int x=5/0;cout<<a+b<<endl;return 0;}",
        'java': "import java.util.*;public class Main{public static void main(String[] args){Scanner sc=new Scanner(System.in);int a=sc.nextInt(),b=sc.nextInt();int x=5/0;System.out.println(a+b);}}"
    },

    'Compilation Error': {
        'python': "print(\"Hello\"",  # missing closing )
        'c': "int main( { return 0; }",  # invalid syntax
        'cpp': "int main( { return 0; }",  # invalid syntax
        'java': "public class Main{public static void main(String[] args){System.out.println(\"Hello\"}}"  # missing )
    },

    'Memory Limit Exceeded': {
        'python': (
            "a = int(input())\n"
            "b = int(input())\n"
            "# Allocate 1GB instantly\n"
            "x = bytearray(5 * 1024 * 1024 * 1024)\n"
            "x[99999999] = 1\n"
            "print(a + b)"
        ),
        'c': """#include <stdio.h>\n#include <stdlib.h>\nint main() {\n    int a, b;\n    scanf("%d %d", &a, &b);\n    int* x = malloc(sizeof(int) * 1024 * 1024 * 512);\n    for (int i = 0; i < 100; i++) x[i] = i; // Access to force actual allocation\n    printf("%d\\n", a + b);\n    return 0;\n}""",

        'cpp': """#include<iostream>\nusing namespace std;\nint main() {\n    int a, b;\n    cin >> a >> b;\n    int* x = new int[1024 * 1024 * 512];\n    for (int i = 0; i < 100; i++) x[i] = i;\n    cout << a + b << endl;\n    return 0;\n}""",

        'java': """import java.util.*;\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int a = sc.nextInt(), b = sc.nextInt();\n        int[][] x = new int[10000][100000]; // Force large allocation\n        System.out.println(a + b);\n    }\n}"""
    }


}

class Command(BaseCommand):
    help = "Test all verdicts in all languages with output checking"

    def handle(self, *args, **kwargs):
        for verdict, lang_map in verdict_cases.items():
            self.stdout.write(f"\n--- Testing {verdict} ---")
            for lang, code in lang_map.items():
                uid = str(uuid.uuid4())
                base_path = Path(settings.BASE_DIR) / 'submission_files' / 'runs' / f"{lang}_{uid}"
                result = run_code_util(code, lang, INPUT, base_path)
                
                actual_output = normalize(result.get("output", ""))
                expected_output = normalize(AC_OUTPUT)
                error = result.get("error")

                if verdict in ['Accepted']:
                    final = "Accepted" if actual_output == expected_output else "Wrong Answer"
                elif verdict == 'Wrong Answer':
                    final = "Wrong Answer" if actual_output != expected_output else "Accepted"
                else:
                    final = error or "Accepted"
                    if final == "Accepted" and actual_output != expected_output:
                        final = "Wrong Answer"

                self.stdout.write(f"[{lang.upper()}] ➜ Expected: {verdict} | Got: {final}")
                
                # For error verdicts, show correct AC code if it failed
                # if verdict not in ['Accepted', 'Wrong Answer'] and final != "Accepted":
                #     self.stdout.write(f"     💡 Use this code for AC:\n{accepted_codes[lang]}\n")
