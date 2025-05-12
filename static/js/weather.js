const uploadForm = document.getElementById('uploadForm')
console.log('元素已经找到:', uploadForm)


document.getElementById('uploadForm').addEventListener('submit', async(event) => {
    event.preventDefault(); // 阻止表单默认提交行为
    console.log('145454545454')

    const fileInput = document.getElementById('csvFile');
    const file = fileInput.files[0];
    // console.log(file)
    if (file) {
        //使用Filereader读取文本内容
        const reader = new FileReader();
        reader.onload = async (e) => {
            console.log('8787878788')
            const text_result = e.target.result;
            const data_list = text_result.split('\r')
            
            const data = data_list
            .filter(row => row.trim() !=='')
            .map(row => row.split(','));
            console.log('ddfdfdfdfdf', data)

            // 发送数据到后端
            try {
                const response = await fetch('/upload_csv', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ data })
                });
                // const result = await response.json();
                console.log('545454545454545454')
                // document.getElementById('status').innerText = '上传成功～';
            } catch (error) {
                console.error('上传失败:', error);
                // document.getElementById('status').innerText = '上传失败，请重试！';
            }
        };
        // console.log(reader)
        reader.readAsText(file);
    } else {
        document.getElementById('output').textContent = '没有选中文件~';
    }
});
