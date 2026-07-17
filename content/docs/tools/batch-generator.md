---
title: "Batch Config Generator"
weight: 5
---

# Batch Config Generator

This tool allows you to automatically generate repetitive configuration scripts or JSON based on a template. 
Define variables in your template using the `{{{VariableName}}}` syntax.

<style>
.generator-container {
    margin-top: 2rem;
    padding: 2rem;
    border: 1px solid var(--gray-200);
    border-radius: 8px;
    background-color: var(--gray-100);
}
.form-group {
    margin-bottom: 1.5rem;
}
.form-group label {
    display: block;
    font-weight: bold;
    margin-bottom: 0.5rem;
}
textarea {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-family: monospace;
    font-size: 0.9rem;
    box-sizing: border-box;
}
input[type="number"] {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
}
.btn {
    background-color: #CF0A2C;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
    display: inline-block;
}
.btn-outline {
    background-color: transparent;
    color: #CF0A2C;
    border: 1px solid #CF0A2C;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
    display: inline-block;
}
.btn:hover, .btn-outline:hover {
    opacity: 0.8;
}
.var-list-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
}
.var-column h4 {
    margin-top: 0;
    margin-bottom: 0.5rem;
}
.alert {
    padding: 1rem;
    background-color: #fee2e2;
    border: 1px solid #ef4444;
    color: #b91c1c;
    border-radius: 4px;
    margin-top: 1rem;
    display: none;
}
</style>

<div class="generator-container">
    <div class="form-group">
        <label>1. Template</label>
        <p style="margin-top: 0; font-size: 0.9em; color: #666;">Use <code>{{{VariableName}}}</code> to define variables. Example provided below.</p>
        <textarea id="templateInput" rows="8">interface {{{var1}}}
 description {{{var2}}}
 port default vlan {{{var3}}}</textarea>
    </div>
    <div class="form-group">
        <button class="btn" onclick="extractVariables()">Extract Variables</button>
    </div>
    <div id="variablesSection" style="display: none;">
        <h3 style="border-bottom: 1px solid #ccc; padding-bottom: 0.5rem;">2. Variable Values</h3>
        <p style="font-size: 0.9em; color: #666;">Enter one value per line for each variable. The number of lines must be at least equal to the loop count.</p>
        <div id="varListContainer" class="var-list-container"></div>
        <h3 style="border-bottom: 1px solid #ccc; padding-bottom: 0.5rem;">3. Loop Count (Max 300)</h3>
        <div class="form-group" style="max-width: 250px;">
            <input type="number" id="loopCount" min="1" max="300" value="3">
        </div>                
        <div id="errorAlert" class="alert"></div>
        <div class="form-group" style="margin-top: 1.5rem;">
            <button class="btn" onclick="generateConfig()">Generate Config</button>
        </div>
    </div>
    <div id="outputSection" class="form-group" style="display: none; margin-top: 2rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #ccc; padding-bottom: 0.5rem; margin-bottom: 0.5rem;">
            <h3 style="margin: 0;">4. Output</h3>
            <button class="btn-outline" id="copyBtn" onclick="copyOutput()">Copy to Clipboard</button>
        </div>
        <textarea id="outputResult" rows="20" readonly style="background-color: #fff;"></textarea>
    </div>
</div>

<script>
let extractedVars = [];

function extractVariables() {
    const template = document.getElementById('templateInput').value;
    const regex = /\{\{\{([^}]+)\}\}\}/g;
    const matches = new Set();
    let match;
    
    while ((match = regex.exec(template)) !== null) {
        matches.add(match[1].trim());
    }
    
    extractedVars = Array.from(matches);
    const container = document.getElementById('varListContainer');
    container.innerHTML = '';
    
    if (extractedVars.length === 0) {
        alert("No variables found in template. Please use {{{VariableName}}} syntax.");
        document.getElementById('variablesSection').style.display = 'none';
        return;
    }
    
    if (extractedVars.length > 12) {
        alert("Error: The maximum number of variables allowed is 12.");
        document.getElementById('variablesSection').style.display = 'none';
        return;
    }

    extractedVars.forEach(varName => {
        const colDiv = document.createElement('div');
        colDiv.className = 'var-column';
        
        const title = document.createElement('h4');
        title.innerText = varName + ' List';
        
        const textarea = document.createElement('textarea');
        textarea.id = 'var_' + varName;
        textarea.rows = 8;
        textarea.placeholder = `Enter values for ${varName}\nOne per line...`;
        
        // Add requested default values
        if (varName === 'var1') {
            textarea.value = "G1/0/1\nG1/0/2\nG1/0/3";
        } else if (varName === 'var2') {
            textarea.value = "Port1\nPort2\nPort3";
        } else if (varName === 'var3') {
            textarea.value = "100\n200\n300";
        }
        
        colDiv.appendChild(title);
        colDiv.appendChild(textarea);
        container.appendChild(colDiv);
    });

    document.getElementById('variablesSection').style.display = 'block';
    document.getElementById('outputSection').style.display = 'none';
    document.getElementById('errorAlert').style.display = 'none';
}

function generateConfig() {
    const loopCount = parseInt(document.getElementById('loopCount').value, 10);
    const alertBox = document.getElementById('errorAlert');
    
    if (isNaN(loopCount) || loopCount < 1 || loopCount > 300) {
        alertBox.innerText = "Error: Loop count must be between 1 and 300.";
        alertBox.style.display = 'block';
        return;
    }

    // Collect all variable arrays
    const varData = {};
    let hasError = false;

    for (const varName of extractedVars) {
        const text = document.getElementById('var_' + varName).value.trim();
        const lines = text.split('\n').map(line => line.trim()).filter(line => line.length > 0);
        
        if (lines.length < loopCount) {
            alertBox.innerText = `Error: Variable "${varName}" has only ${lines.length} values, but loop count is ${loopCount}. Please provide at least ${loopCount} values.`;
            alertBox.style.display = 'block';
            hasError = true;
            break;
        }
        varData[varName] = lines;
    }

    if (hasError) return;
    
    alertBox.style.display = 'none';
    
    const template = document.getElementById('templateInput').value;
    let finalOutput = [];

    for (let i = 0; i < loopCount; i++) {
        let currentIter = template;
        for (const varName of extractedVars) {
            // Replace all occurrences of {{{varName}}}
            const regex = new RegExp('\\{\\{\\{' + varName + '\\}\\}\\}', 'g');
            currentIter = currentIter.replace(regex, varData[varName][i]);
        }
        finalOutput.push(currentIter);
    }

    // Join with double newline to separate objects clearly
    document.getElementById('outputResult').value = finalOutput.join('\n\n');
    document.getElementById('outputSection').style.display = 'block';
    
    // Reset copy button text
    const copyBtn = document.getElementById('copyBtn');
    if (copyBtn) {
        copyBtn.innerText = 'Copy to Clipboard';
    }
}

function copyOutput() {
    const outputText = document.getElementById('outputResult');
    outputText.select();
    outputText.setSelectionRange(0, 99999); /* For mobile devices */
    
    try {
        document.execCommand('copy');
        const copyBtn = document.getElementById('copyBtn');
        if (copyBtn) {
            copyBtn.innerText = 'Copied!';
            setTimeout(() => {
                copyBtn.innerText = 'Copy to Clipboard';
            }, 2000);
        }
    } catch (err) {
        alert("Failed to copy text.");
    }
}
</script>
