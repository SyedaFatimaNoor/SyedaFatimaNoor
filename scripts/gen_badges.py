#!/usr/bin/env python3
"""Generate the Languages & Tools badge section, validating slugs against the
live simple-icons index. Invalid logo slugs are dropped (text-only badge)."""

import json
import urllib.request

BADGES = {
    "Languages": [
        ("Python", "3776AB", "python"), ("JavaScript", "F7DF1E", "javascript"),
        ("TypeScript", "3178C6", "typescript"), ("C", "A8B9CC", "c"),
        ("C++", "00599C", "cplusplus"), ("C#", "239120", None),
        ("Java", "E76F00", None), ("Kotlin", "7F52FF", "kotlin"),
        ("Go", "00ADD8", "go"), ("Rust", "DEA584", "rust"),
        ("Swift", "F05138", "swift"), ("PHP", "777BB4", "php"),
        ("Ruby", "CC342D", "ruby"), ("Dart", "0175C2", "dart"),
        ("SQL", "4169E1", None), ("Bash", "4EAA25", "gnubash"),
        ("PowerShell", "5391FE", None), ("R", "276DC3", "r"),
        ("HTML5", "E34F26", "html5"), ("CSS3", "1572B6", "css"),
    ],
    "Frontend": [
        ("React", "61DAFB", "react"), ("Next.js", "000000", "nextdotjs"),
        ("Vue", "4FC08D", "vuedotjs"), ("Angular", "DD0031", "angular"),
        ("Svelte", "FF3E00", "svelte"), ("Tailwind", "06B6D4", "tailwindcss"),
        ("Bootstrap", "7952B3", "bootstrap"), ("Sass", "CC6699", "sass"),
        ("Less", "1D365D", "less"), ("jQuery", "0769AD", "jquery"),
        ("Redux", "764ABC", "redux"), ("Webpack", "8DD6F9", "webpack"),
        ("Vite", "646CFF", "vite"), ("Astro", "FF5D01", "astro"),
        ("Electron", "47848F", "electron"), ("Framer", "0055FF", "framer"),
        ("Styled Components", "DB7093", "styledcomponents"),
        ("Material UI", "007FFF", "mui"),
    ],
    "Backend": [
        ("Node.js", "339933", "nodedotjs"), ("Express", "000000", "express"),
        ("Flask", "000000", "flask"), ("Django", "092E20", "django"),
        ("FastAPI", "009688", "fastapi"), ("Spring Boot", "6DB33F", "springboot"),
        ("Laravel", "FF2D20", "laravel"), (".NET", "512BD4", "dotnet"),
        ("Rails", "CC0000", "rubyonrails"), ("GraphQL", "E10098", "graphql"),
        ("Prisma", "2D3748", "prisma"), ("Socket.io", "010101", "socketdotio"),
        ("Redis", "FF4438", "redis"), ("Nginx", "009639", "nginx"),
        ("Apache Kafka", "231F20", "apachekafka"), ("Docker", "2496ED", "docker"),
        ("REST API", "009688", None), ("gRPC", "244C5A", None),
    ],
    "Mobile": [
        ("Flutter", "02569B", "flutter"), ("Dart", "0175C2", "dart"),
        ("React Native", "61DAFB", "reactnative"), ("Swift", "F05138", "swift"),
        ("Kotlin", "7F52FF", "kotlin"), ("Android", "3DDC84", "android"),
        ("Apple", "000000", "apple"), ("Expo", "000020", "expo"),
        ("Ionic", "3880FF", "ionic"), ("Firebase", "FFCA28", "firebase"),
        ("Unity", "FFFFFF", "unity"), ("Godot", "478CBF", "godot"),
    ],
    "Databases": [
        ("MySQL", "4479A1", "mysql"), ("PostgreSQL", "4169E1", "postgresql"),
        ("MongoDB", "47A248", "mongodb"), ("SQLite", "003B57", "sqlite"),
        ("Redis", "FF4438", "redis"), ("MariaDB", "003545", "mariadb"),
        ("Cassandra", "1287B1", "cassandra"), ("Elasticsearch", "005571", "elasticsearch"),
        ("Oracle", "F80000", None), ("MS SQL Server", "CC2927", None),
    ],
    "Cloud & DevOps": [
        ("AWS", "FF9900", None), ("Azure", "0078D4", None),
        ("Google Cloud", "4285F4", "googlecloud"), ("Docker", "2496ED", "docker"),
        ("Kubernetes", "326CE5", "kubernetes"), ("Terraform", "7B42BC", "terraform"),
        ("Ansible", "EE0000", "ansible"), ("Jenkins", "D24939", "jenkins"),
        ("GitHub Actions", "2088FF", "githubactions"), ("Git", "F05032", "git"),
        ("GitLab", "FC6D26", "gitlab"), ("Vercel", "000000", "vercel"),
        ("Netlify", "00C7B7", "netlify"), ("Cloudflare", "F38020", "cloudflare"),
        ("Nginx", "009639", "nginx"), ("Linux", "FCC624", "linux"),
    ],
    "AI/ML": [
        ("TensorFlow", "FF6F00", "tensorflow"), ("PyTorch", "EE4C2C", "pytorch"),
        ("scikit-learn", "F7931E", "scikitlearn"), ("Pandas", "150458", "pandas"),
        ("NumPy", "013243", "numpy"), ("OpenCV", "5C3EE8", "opencv"),
        ("Hugging Face", "FFD21E", "huggingface"), ("Jupyter", "F37626", "jupyter"),
        ("Keras", "D00000", "keras"), ("OpenAI", "412991", None),
        ("LangChain", "1C3C3C", "langchain"), ("Streamlit", "FF4B4B", "streamlit"),
    ],
    "Tools & IDEs": [
        ("VS Code", "007ACC", None), ("PyCharm", "000000", "pycharm"),
        ("IntelliJ IDEA", "000000", "intellijidea"), ("Vim", "019733", "vim"),
        ("Neovim", "57A143", "neovim"), ("Git", "F05032", "git"),
        ("GitHub", "181717", "github"), ("Postman", "FF6C37", "postman"),
        ("Figma", "F24E1E", "figma"), ("Notion", "000000", "notion"),
        ("Jupyter", "F37626", "jupyter"), ("Anaconda", "44A833", "anaconda"),
        ("Jira", "0052CC", "jira"), ("Trello", "0052CC", "trello"),
        ("Stack Overflow", "F58025", "stackoverflow"), ("Windows", "0078D6", "windows"),
        ("Ubuntu", "E95420", "ubuntu"),
    ],
}


def fetch_index():
    url = "https://unpkg.com/simple-icons@16.28.0/data/simple-icons.json"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    data = json.load(urllib.request.urlopen(req, timeout=60))
    return {e["slug"] for e in data}


def main():
    slugs = fetch_index()
    total = dropped = 0
    dropped_names = []
    print("## Languages & Tools")
    for group, items in BADGES.items():
        print(f"\n### {group}\n")
        for name, color, slug in items:
            total += 1
            logo = f"&logo={slug}&logoColor=white" if slug in slugs else ""
            if slug and slug not in slugs:
                dropped += 1
                dropped_names.append(name)
            label = name.replace(" ", "%20")
            url = f"https://img.shields.io/badge/{label}-{color}?style=for-the-badge{logo}"
            print(f"![{name}]({url})")
    print(f"\n<!-- generated badges: {total}, logos dropped: {dropped} {dropped_names} -->")


if __name__ == "__main__":
    main()