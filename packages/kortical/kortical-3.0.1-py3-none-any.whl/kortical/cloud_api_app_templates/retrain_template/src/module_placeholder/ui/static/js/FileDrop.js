import { get_base_url } from "./helpers/BaseUrl.js";

const template = document.createElement('template');
template.innerHTML = `
    <style>
        #file-drop__wrapper {
            background: var(--bg-secondary);
            border-radius: 8px;
            border: 1px solid var(--bg-form);
            padding: 30px;
        }
        #file-drop__wrapper h1 {
            text-transform: capitalize;
        }
        #file-drop__wrapper .status-display {
            color: var(--success);
        }
        #file-drop__wrapper .action-button {
            text-transform: capitalize;
        }
        .file-drop-area {
            border: 2px dashed var(--secondary);
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            min-height: 200px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .file-input {
            display: none;
        }
        .file-name {
            margin-top: 10px;
        }
        .file-upload-label {
            color: var(--secondary);
            cursor: pointer;
            font-weight: 600;
        }
    </style>
    <div id="file-drop__wrapper">
        <h1 class="text-center mb-2"></h1>
        <div class="status-display w-100 text-center mb-3"></div>
        <div class="file-drop-area mb-2">
            <div id="file-drop__text">
                Drag & Drop <br/>or<br/><label for="file-upload" class="file-upload-label">Browse</label>
                <input type="file" id="file-upload" class="file-input" />
            </div>
        </div>
        <div class="file-name mb-3"></div>
        <button class="action-button btn btn-secondary mb-0"></button>
    </div>
`;

class FileDrop extends HTMLElement {
    constructor() {
        super();

        this.uploaded_file = null;
    }

    set_mode(mode) {
        this.mode = mode;
        const action_button = this.querySelector('.action-button');
        action_button.innerText = mode === 'predict' ? 'Predict' : 'Train';
        action_button.onclick = mode === 'predict' ? () => this.predict() : () => this.train();
    }

    handle_drag_over(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    handle_file_drop(e) {
        e.preventDefault();
        e.stopPropagation();

        const files = e.dataTransfer.files;
        if (files.length) {
            this.display_file_name(files[0]);
        }
    }

    handle_file_select(e) {
        const files = e.target.files;
        if (files.length) {
            this.display_file_name(files[0]);
        }
    }

    display_file_name(file) {
        this.uploaded_file = file;
        this.file_name_display.textContent = `Uploaded file: ${file.name}`;
    }

    on_action_clicked() {
        this.mode === 'predict' ? this.predict() : this.train();
    }

    async predict() {
        this.action_button.disabled = true;

        const form_data = new FormData();
        form_data.append('file', this.uploaded_file);

        try {
            const response = await fetch(`${get_base_url()}/predict`, {
                method: 'POST',
                body: form_data
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'prediction.csv';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            } else {
                console.error('Error in prediction request');
            }
        } catch (error) {
            console.error('Network error:', error);
        }

        this.action_button.disabled = false;
        this.reset_component();
    }

    async train() {
        this.action_button.disabled = true;
        this.status_display.textContent = 'Starting training...';
        const form_data = new FormData();
        form_data.append('file', this.uploaded_file);

        try {
            // First POST to /online_learning
            let response = await fetch(`${get_base_url()}/online_learning`, {
                method: 'POST',
                body: form_data
            });
            let result = await response.json();
            if (result.result !== 'success') {
                this.action_button.disabled = false;
                throw new Error('Error in /online_learning');
            }

            // Second POST to /train
            response = await fetch(`${get_base_url()}/train?api_key=${window.api_key}`, { method: 'POST' });
            result = await response.json();
            const train_id = result.train_id;

            if (result.error) {
                this.status_display.textContent = result.error;
                throw new Error(result.error);
            }

            // Polling /train/{train_id}
            const poll = async (train_id) => {
                const train_response = await fetch(`${get_base_url()}/train/${train_id}?api_key=${window.api_key}`);
                const train_result = await train_response.json();
                this.status_display.textContent = `Status: ${train_result.status}`;
                if (train_result.status === 'complete') {
                    this.action_button.disabled = false;
                } else {
                    setTimeout(() => poll(train_id), 2000);
                }
            };
            await poll(train_id);
        } catch (error) {
            console.error('Training error:', error);
            this.status_display.textContent = 'Training failed.';
        }
    }

    reset_component() {
        this.uploaded_file = null;
        this.querySelector('.file-name').textContent = '';
        this.querySelector('.status-display').textContent = '';
    }

    connectedCallback() {
        this.appendChild(template.content.cloneNode(true));
        this.mode = this.getAttribute('mode');
        this.title_element = this.querySelector('h1');
        this.file_input = this.querySelector('.file-input');
        this.file_input_label = this.querySelector('.file-upload-label');
        this.file_drop_area = this.querySelector('.file-drop-area');
        this.file_name_display = this.querySelector('.file-name');
        this.action_button = this.querySelector('.action-button');
        this.status_display = this.querySelector('.status-display');

        this.action_button.innerText = this.mode;
        this.title_element.innerText = this.mode;
        this.file_input_label.setAttribute('for', `file-upload__${this.mode}`);
        this.file_input.id = `file-upload__${this.mode}`;

        this.file_drop_area.addEventListener('dragover', (e) => this.handle_drag_over(e));
        this.file_drop_area.addEventListener('drop', (e) => this.handle_file_drop(e));
        this.file_input.addEventListener('change', (e) => this.handle_file_select(e));
        this.action_button.addEventListener('click', () => this.on_action_clicked());
    }

    disconnectedCallback() {
        this.file_drop_area.removeEventListener('dragover', (e) => this.handle_drag_over(e));
        this.file_drop_area.removeEventListener('drop', (e) => this.handle_file_drop(e));
        this.file_input.removeEventListener('change', (e) => this.handle_file_select(e));
        this.action_button.removeEventListener('click', () => this.on_action_clicked());
    }
}

window.customElements.define("k-file-drop", FileDrop);
