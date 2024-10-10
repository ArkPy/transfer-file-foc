import os
import wexpect
from flask import Flask, render_template, request, redirect, url_for, flash
#transfer file

app = Flask(__name__)
app.secret_key = 'some_secret_key'  # Required for flashing messages

# Folder to temporarily save uploaded files
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the uploaded file and password from the form
        uploaded_file = request.files['file_path']
        password = request.form['password']

        if uploaded_file:
            # Replace spaces with underscores in the file name
            filename = uploaded_file.filename.replace(' ', '_')
            
            # Save the file temporarily in the server with the new name
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(file_path)

            # Define the SCP command, including the renamed file
            scp_command = f'scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {file_path} AKRAM@192.168.1.101:C:\\Users\\AKRAM\\Desktop\\Receiver'

            try:
                # Automate SCP process with wexpect to handle password input
                child = wexpect.spawn(scp_command)
                child.expect("password:")  # Wait for the password prompt
                child.sendline(password)   # Send the password
                child.expect(wexpect.EOF)  # Wait for the process to finish

                # Flash success message after successful transfer
                flash('File transferred successfully!', 'success')
            except Exception as e:
                flash(f'File transfer failed: {str(e)}', 'danger')

            # Redirect back to the form page after processing
            return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
