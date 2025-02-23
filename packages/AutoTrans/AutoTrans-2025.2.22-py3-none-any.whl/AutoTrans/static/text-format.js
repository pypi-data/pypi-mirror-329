async function format(textarea) {
    var article = textarea.value.trim();

    if (textarea.getAttribute('operations')) {
        article = await post('/xml_reformat', {
            xml: article,
            operations: textarea.getAttribute('operations')
        });
    }

    var level1 = textarea.getAttribute('xml-label');
    var level2 = '';
    if (level1.includes('|')) {
        [level1, level2] = level1.split('|');
        level2 = level2.split('_?')[0];
    }
    else if (level1.includes('_?')) {
        level2 = level1.split('_?')[0];
        level1 = ''
    }

    if (article != "") {     
        // 使用正则表达式将上一行尾的空白字符和下一行的换行符替换为一个换行符
        article = article.replace(/[ \t]*\n/g, "\n");
        // 使用正则表达式将超过两个连续的换行符替换为两个连续换行符
        article = article.replace(/\n{2,}/g, "\n\n");

        // 如果有level1标签，就摘取level1标签内的内容以供后面处理；否则就摘取整个字符串
        level1_text = article;
        if (level1 != "") {
            var level1_text = new RegExp(`<${level1}>\n?([\\s\\S]*?)\n?<\\/${level1}>`, 'g').exec(article);
            if (level1_text) {
                level1_text = level1_text[1];
            }
        }

        // 如果有level2标签，就去除标签之间的连续换行符
        if (level1_text.includes(`<${level2}_`)&&level1_text.includes(`</${level2}_`)) {
            level1_text = level1_text.replace(/>\n{0,}</g, ">\n<");
            level1_text = level1_text.replace(/\n\n/g, ""); //去除两次输出（由continue衔接）造成的双换行符
        }
        else if (level2 != '') {
            // 使用正则表达式捕获连续换行符及其前后的内容
            matches = article.match(/(.|\n)+?(\n{2,}|$)/g);
            // 使用捕获的内容进行分段
            paragraphs = matches.map((paragraph, index) => {
                return `<${level2}_${index + 1}>${paragraph.trim()}\n</${level2}_${index + 1}>`;
            });
            level1_text = paragraphs.join('\n');
        }

        if (level1 == "") {
            textarea.value = level1_text;
        }
        else {
            textarea.value = `<${level1}>\n${level1_text}\n</${level1}>`;
        }

    }
    return textarea.value
}

document.getElementById('format_annotation').addEventListener('click', async function() {
        document.getElementById('glossary').value = '| Term | Category | Translation |' + document.getElementById('chinese_annotation').value.match(/Term\s*\|\s*Category\s*\|\s*Translation\s*\|([\s\S]*\|)[^|]*<注释>/)[1]
        // 使用按钮上的 textarea-id 属性获取对应的 textarea ID
        let textarea = document.getElementById(this.getAttribute('textarea-id'));
        document.getElementById('wording').value = /<风格>(.*?)<\/风格>/g.exec(textarea.value)[1];
        document.getElementById('category').value = /<分类>(.*?)<\/分类>/g.exec(textarea.value)[1];
        document.getElementById('polish_solution').value = /<润色方案>(.*?)<\/润色方案>/gs.exec(textarea.value)[1];
    });

document.querySelectorAll('.format_article').forEach(button => {
    button.addEventListener('click', function() {
        // 使用按钮上的 textarea-id 属性获取对应的 textarea ID
        let textarea = document.getElementById(this.getAttribute('textarea-id'));
        format(textarea);
    });
});