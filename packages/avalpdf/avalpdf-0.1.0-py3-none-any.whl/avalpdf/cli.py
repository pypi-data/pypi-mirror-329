#!/usr/bin/env python3

import argparse
import json
from pathlib import Path
import sys
from pdfixsdk import *
import ctypes
from typing import Dict, List, Tuple
import tempfile
import urllib.request
import urllib.parse

# ANSI color codes
COLOR_GREEN = '\033[32;1m'    # P tags (verde brillante)
COLOR_RED = '\033[38;5;204m'  # Headings (rosa chiaro)
COLOR_ORANGE = '\033[33;1m'   # Figures (arancione brillante)
COLOR_PURPLE = '\033[35;1m'   # Tables (viola brillante)
COLOR_BLUE = '\033[34;1m'     # Lists (blu brillante)
COLOR_RESET = '\033[0m'       # Reset color

def pdf_to_json(pdf_path):
    """Convert PDF to JSON using PDFix SDK"""
    pdfix = GetPdfix()
    doc = pdfix.OpenDoc(pdf_path, "")
    
    if doc is None:
        raise Exception("Failed to open PDF document")
    
    # Prepare PDF to JSON conversion params
    params = PdfJsonParams()
    params.flags = (kJsonExportStructTree | kJsonExportDocInfo | kJsonExportText)
    
    # Convert to JSON
    json_conv = doc.CreateJsonConversion()
    json_conv.SetParams(params)
    
    # Extract data to stream
    mem_stm = pdfix.CreateMemStream()
    json_conv.SaveToStream(mem_stm)
    
    # Read memory stream into bytearray
    sz = mem_stm.GetSize()
    data = bytearray(sz)
    raw_data = (ctypes.c_ubyte * sz).from_buffer(data)
    mem_stm.Read(0, raw_data, len(raw_data))
    
    # Cleanup
    mem_stm.Destroy()
    doc.Close()
    
    return json.loads(data.decode("utf-8"))

def extract_content(element, level=0):
    results = []
    
    # Skip if element is not a dictionary
    if not isinstance(element, dict):
        return results
        
    tag_type = element.get('S', '')
    
    try:
        # Gestione speciale per tag Part
        if tag_type == 'Part':
            if 'K' in element and isinstance(element.get('K'), list):
                for child in element.get('K', []):
                    if isinstance(child, dict):
                        nested_results = extract_content(child, level)
                        results.extend(nested_results)
            return results
            
        if tag_type and tag_type != 'Document':
            content = []
            child_elements = []
            
            # Crea l'elemento base solo con il tag
            element_dict = {"tag": tag_type}
            
            if tag_type == 'Figure':
                alt_text = element.get('Alt', '')
                element_dict["text"] = alt_text if alt_text else ""
                results.append(element_dict)
                return results
                
            elif tag_type == 'Table':
                table_content = {
                    'headers': [],
                    'rows': []
                }
                if 'K' in element:
                    for row in element['K']:
                        if row.get('S') == 'TR':
                            header_row = []
                            data_row = []
                            for cell in row.get('K', []):
                                cell_type = cell.get('S', '')
                                cell_content = []
                                
                                # Process cell content recursively to capture all nested elements
                                def process_cell_content(cell_elem):
                                    if isinstance(cell_elem, dict):
                                        if cell_elem.get('S') == 'P':
                                            # Create a paragraph element even if empty
                                            p_content = []
                                            if 'K' in cell_elem:
                                                for k in cell_elem.get('K', []):
                                                    if isinstance(k, dict):
                                                        if 'Content' in k:
                                                            for content_item in k['Content']:
                                                                if content_item.get('Type') == 'Text':
                                                                    text = content_item.get('Text', '').strip()
                                                                    if text:
                                                                        p_content.append(text)
                                            return {
                                                "tag": "P",
                                                "text": " ".join(p_content) if p_content else ""
                                            }
                                        elif 'K' in cell_elem:
                                            results = []
                                            for k in cell_elem.get('K', []):
                                                processed = process_cell_content(k)
                                                if processed:
                                                    if isinstance(processed, list):
                                                        results.extend(processed)
                                                    else:
                                                        results.append(processed)
                                            return results
                                    return None

                                # Process cell content and flatten nested arrays
                                processed_content = process_cell_content(cell)
                                if processed_content:
                                    if isinstance(processed_content, list):
                                        cell_content.extend(processed_content)
                                    else:
                                        cell_content.append(processed_content)
                                
                                # If no content was processed, add an empty paragraph
                                if not cell_content:
                                    cell_content.append({
                                        "tag": "P",
                                        "text": ""
                                    })
                                
                                # Add cell to appropriate section
                                if cell_type == 'TH':
                                    header_row.extend(cell_content)
                                elif cell_type == 'TD':
                                    data_row.extend(cell_content)
                            
                            # Add row to appropriate section
                            if header_row:
                                table_content['headers'].append(header_row)
                            if data_row:
                                table_content['rows'].append(data_row)
                
                results.append({
                    "tag": "Table",
                    "content": table_content
                })
            
            elif tag_type == 'L':
                items = []
                is_ordered = False
                
                if 'K' in element:
                    for item in element.get('K', []):
                        if item.get('S') == 'LI':
                            # Estrai separatamente label e corpo dell'elemento lista
                            label = ""
                            body_text = []
                            
                            for li_child in item.get('K', []):
                                if li_child.get('S') == 'Lbl':
                                    # Estrai il bullet/numero
                                    for k in li_child.get('K', []):
                                        if isinstance(k, dict) and 'Content' in k:
                                            for content_item in k['Content']:
                                                if content_item.get('Type') == 'Text':
                                                    label += content_item.get('Text', '').strip()
                                    if label.replace('.', '').isdigit():
                                        is_ordered = True
                                        
                                elif li_child.get('S') == 'LBody':
                                    # Estrai il testo del corpo ricorsivamente preservando spazi
                                    def process_list_body(element):
                                        if isinstance(element, dict):
                                            if 'Content' in element:
                                                for content_item in element['Content']:
                                                    if content_item.get('Type') == 'Text':
                                                        text = content_item.get('Text', '')
                                                        # Aggiungi il testo senza strip() per preservare gli spazi
                                                        body_text.append(text)
                                            elif 'K' in element:
                                                for child in element['K']:
                                                    process_list_body(child)
                                    
                                    for p in li_child.get('K', []):
                                        process_list_body(p)
                                                                
                            # Combina label e body preservando gli spazi corretti
                            full_text = ''.join(body_text).strip()
                            if label and full_text:
                                items.append(f"{label} {full_text}")
                            elif full_text:
                                items.append(full_text)
                            elif label:
                                items.append(label)

                if items:
                    results.append({
                        "tag": "L",
                        "ordered": is_ordered,
                        "items": items
                    })
                return results

            else:
                # Process children first to collect nested elements
                if 'K' in element:
                    for child in element.get('K', []):
                        if not isinstance(child, dict):
                            continue
                            
                        if 'Content' in child:
                            try:
                                # Collect text fragments preserving exact spacing
                                text_fragments = []
                                for content_item in child.get('Content', []):
                                    if content_item.get('Type') == 'Text':
                                        # Add text exactly as is, without stripping
                                        text_fragments.append(content_item.get('Text', ''))
                                if text_fragments:
                                    # Join fragments without modifying spaces
                                    content.append(''.join(text_fragments))
                            except (KeyError, AttributeError):
                                continue
                        else:
                            nested_results = extract_content(child, level + 1)
                            child_elements.extend(nested_results)
                
                # Create element with text and children
                # Join content fragments without modifying spaces
                text = ''.join(content)
                
                # Add text only if non-empty
                if text or text == '':  # Include empty strings
                    element_dict["text"] = text
                if child_elements:
                    element_dict["children"] = child_elements
                    
                results.append(element_dict)
        
        # Process siblings for Document tag
        elif 'K' in element and isinstance(element.get('K'), list):
            for child in element.get('K', []):
                if isinstance(child, dict):  # Verifica esplicita che child sia un dict
                    nested_results = extract_content(child, level + 1)
                    results.extend(nested_results)
                    
    except Exception as e:
        print(f"Warning: Error processing element: {str(e)}", file=sys.stderr)
        
    return results

def extract_list_item_text(item):
    """Helper function to extract text from list items safely"""
    try:
        if item.get('S') != 'LI':
            return None

        bullet = ""
        text_fragments = []
        
        # Extract bullet and text from LI structure
        for child in item.get('K', []):
            if child.get('S') == 'Lbl':
                # Extract bullet point
                for k in child.get('K', []):
                    if isinstance(k, dict) and 'Content' in k:
                        for content_item in k['Content']:
                            if content_item.get('Type') == 'Text':
                                bullet = content_item.get('Text', '').strip()
                                
            elif child.get('S') == 'LBody':
                # Process each paragraph in LBody
                for p in child.get('K', []):
                    if isinstance(p, dict):
                        if p.get('S') == 'P':
                            # Process paragraph content preserving spaces
                            for k in p.get('K', []):
                                if isinstance(k, dict):
                                    if 'Content' in k:
                                        # Add each text fragment, including spaces
                                        for content_item in k['Content']:
                                            if content_item.get('Type') == 'Text':
                                                text_fragments.append(content_item.get('Text', ''))
                                    elif k.get('S') in ['Span', 'Link']:
                                        for span_k in k.get('K', []):
                                            if isinstance(span_k, dict) and 'Content' in span_k:
                                                for content_item in span_k['Content']:
                                                    if content_item.get('Type') == 'Text':
                                                        text_fragments.append(content_item.get('Text', ''))

        # Join all text fragments directly, preserving spaces
        text = ''.join(text_fragments).strip()
        
        # Handle different list marker formats
        if bullet:
            if bullet in ['•', '-', '*']:  # Common bullet points
                return f"{bullet} {text}" if text else bullet
            elif bullet.isdigit() or bullet.rstrip('.').isdigit():  # Numbered lists
                return f"{bullet} {text}" if text else bullet
            else:  # Other markers
                return f"{bullet} {text}" if text else bullet
        
        return text if text else None
                
    except Exception as e:
        print(f"Warning: Error extracting list item text: {str(e)}", file=sys.stderr)
        
    return None

def create_simplified_json(pdf_json, results):
    """Create simplified JSON including metadata from full JSON"""
    metadata_fields = [
        "creation_date", "mod_date", "author", "title", "subject",
        "keywords", "producer", "creator", "standard", "lang",
        "num_pages", "tagged"
    ]
    
    simplified = {
        "metadata": {
            field: pdf_json.get(field, "") for field in metadata_fields
        },
        "content": results
    }
    return simplified

def print_formatted_content(element, level=0):
    """Stampa il contenuto in modo leggibile con indentazione"""
    indent = "  " * level
    
    if element.get('tag') == 'Figure':
        print(f"{indent}{COLOR_ORANGE}[Figure]{COLOR_RESET} {element.get('text', '')}")
        return

    if element.get('tag') == 'Table':
        print(f"{indent}{COLOR_PURPLE}[Table]{COLOR_RESET}")
        
        # Print headers if present
        if element['content']['headers']:
            print(f"{indent}  {COLOR_PURPLE}[Header]{COLOR_RESET}")
            for header_row in element['content']['headers']:
                row_text = []
                for cell in header_row:
                    if isinstance(cell, dict):
                        tag = f"{COLOR_GREEN}[{cell['tag']}]{COLOR_RESET} " if 'tag' in cell else ""
                        if 'children' in cell:
                            nested = [f"{child['text']}" for child in cell['children']]
                            row_text.append(f"{tag}{cell.get('text', '')} -> {' '.join(nested)}")
                        else:
                            row_text.append(f"{tag}{cell.get('text', '')}")
                    else:
                        row_text.append(str(cell))
                print(f"{indent}    {' | '.join(row_text)}")
        
        # Print data rows
        if element['content']['rows']:
            print(f"{indent}  {COLOR_PURPLE}[Data]{COLOR_RESET}")
            for row in element['content']['rows']:
                row_text = []
                for cell in row:
                    if isinstance(cell, dict):
                        tag = f"{COLOR_GREEN}[{cell['tag']}]{COLOR_RESET} " if 'tag' in cell else ""
                        if 'children' in cell:
                            nested = [f"{child['text']}" for child in cell['children']]
                            row_text.append(f"{tag}{cell.get('text', '')} -> {' '.join(nested)}")
                        else:
                            row_text.append(f"{tag}{cell.get('text', '')}")
                    else:
                        row_text.append(str(cell))
                print(f"{indent}    {' | '.join(row_text)}")
        return

    if element.get('tag') == 'L':
        list_type = f"{COLOR_BLUE}[ORDERED LIST]{COLOR_RESET}" if element.get('ordered', False) else f"{COLOR_BLUE}[UNORDERED LIST]{COLOR_RESET}"
        print(f"{indent}{list_type}")
        if element.get('items'):
            if element.get('ordered', False):
                for i, item in enumerate(element.get('items'), 1):
                    if not item.startswith(str(i)):
                        print(f"{indent}  {i}. {item}")
                    else:
                        print(f"{indent}  {item}")
            else:
                for item in element.get('items'):
                    print(f"{indent}  {item}")
        return

    # Gestione standard per altri tag
    tag = element['tag']
    if tag == 'P':
        tag_str = f"{COLOR_GREEN}[{tag}]{COLOR_RESET}"
    elif tag.startswith('H'):
        tag_str = f"{COLOR_RED}[{tag}]{COLOR_RESET}"
    else:
        tag_str = f"[{tag}]"
        
    text = element.get('text', '')
    children = element.get('children', [])
    
    if children:
        child_texts = []
        for child in children:
            if child.get('tag') == 'Link':
                if 'url' in child:
                    child_texts.append(f"[LINK][{child.get('url')}]: {child.get('text')}")
                else:
                    child_texts.append(f"[LINK] {child.get('text')}")
            elif child.get('tag') == 'Figure':
                child_texts.append(f"{COLOR_ORANGE}[IMAGE]{COLOR_RESET} {child.get('text', '')}")
            elif child.get('tag') == 'Span':
                child_texts.append(f"[SPAN] {child.get('text', '')}")
            else:
                child_texts.append(child.get('text', ''))
        
        # Stampa con indentazione quando c'è sia testo che figure
        has_figures = any(child.get('tag') == 'Figure' for child in children)
        if has_figures and text:
            print(f"{indent}{tag_str} {text}")
            print(f"{indent}  -> {', '.join(child_texts)}")
        else:
            if text:
                print(f"{indent}{tag_str} {text} -> {', '.join(child_texts)}")
            else:
                print(f"{indent}{tag_str} -> {', '.join(child_texts)}")
    else:
        print(f"{indent}{tag_str} {text}")


def is_only_whitespace(text: str) -> bool:
    """Helper function to check if text contains only whitespace characters"""
    return bool(text and all(c in ' \t\n\r' for c in text))

class AccessibilityValidator:
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.successes = []
        self.is_tagged = False
        
        # Definizione dei pesi per ogni tipo di controllo
        self.check_weights = {
            'tagging': 15,        # Il tagging è fondamentale per l'accessibilità
            'title': 10,          # Il titolo è importante per la navigazione
            'language': 10,       # La lingua è importante per screen reader
            'headings': 12,       # La struttura dei titoli è essenziale
            'figures': 10,        # Le immagini necessitano di alt text
            'tables': 12,         # Le tabelle richiedono una struttura corretta
            'lists': 8,           # Le liste devono essere ben strutturate
            'empty_elements': 5,  # Gli elementi vuoti sono meno critici
            'underlining': 3,     # L'uso di underscore è minore
            'spacing': 3,         # Lo spaziamento delle maiuscole è minore
            'extra_spaces': 5     # Spazi multipli usati per layout
        }
        self.check_scores = {k: 0 for k in self.check_weights}

    def validate_metadata(self, metadata: Dict) -> None:
        # Check tagged status first
        tagged = metadata.get('tagged')
        if not tagged or tagged.lower() != 'true':
            self.issues.append("Document is not tagged")
            self.check_scores['tagging'] = 0
            self.is_tagged = False
        else:
            self.successes.append("Document is tagged")
            self.check_scores['tagging'] = 100
            self.is_tagged = True
            
        # Check title
        if not metadata.get('title'):
            self.issues.append("Title is missing or empty")
            self.check_scores['title'] = 0
        else:
            self.successes.append("Document has a title")
            self.check_scores['title'] = 100
            
        # Check language
        lang = metadata.get('lang', '').lower()
        if not lang.startswith('it'):
            self.issues.append(f"Document language is not Italian (found: {lang})")
            self.check_scores['language'] = 0
        else:
            self.successes.append("Document language is Italian")
            self.check_scores['language'] = 100

    def validate_empty_elements(self, content: List) -> None:
        """Check for any empty elements in the document"""
        if not self.is_tagged:
            self.check_scores['empty_elements'] = 0
            return
            
        # Dizionari per conteggiare elementi vuoti per tipo e relativi percorsi
        empty_counts = {
            'paragraphs': {'empty': 0, 'whitespace': 0, 'paths': []},
            'headings': {'empty': 0, 'whitespace': 0, 'paths': []},
            'spans': {'empty': 0, 'whitespace': 0, 'paths': []},
            'tables': {'count': 0, 'paths': []},
            'table_cells': {'count': 0, 'paths': []},
            'lists': {'count': 0, 'paths': []},
            'list_items': {'count': 0, 'paths': []}
        }
        
        table_count = 0
        
        def check_element(element: Dict, path: str = "") -> None:
            tag = element.get('tag', '')
            text = element.get('text', '')
            children = element.get('children', [])
            
            current_path = f"{path}/{tag}" if path else tag
            
            # Un elemento è considerato vuoto se:
            # 1. Non ha testo o ha solo spazi/tab
            # 2. Non ha figli
            has_no_content = not text.strip() and not children
            has_only_whitespace = is_only_whitespace(text) and not children
            
            # Controllo specifico per tipo di elemento
            if has_no_content or has_only_whitespace:
                if tag.startswith('H'):
                    if has_only_whitespace:
                        empty_counts['headings']['whitespace'] += 1
                    else:
                        empty_counts['headings']['empty'] += 1
                    empty_counts['headings']['paths'].append(current_path)
                elif tag == 'P':
                    if has_only_whitespace:
                        empty_counts['paragraphs']['whitespace'] += 1
                    else:
                        empty_counts['paragraphs']['empty'] += 1
                    empty_counts['paragraphs']['paths'].append(current_path)
                elif tag == 'Span':
                    if has_only_whitespace:
                        empty_counts['spans']['whitespace'] += 1
                    else:
                        empty_counts['spans']['empty'] += 1
                    empty_counts['spans']['paths'].append(current_path)
            
            # Gestione speciale per tabelle e altri elementi strutturali
            # (resto del codice per tabelle e liste rimane invariato)
            # ...existing code for table and list checks...
        
        for element in content:
            check_element(element)
        
        # Genera reports raggruppati
        # Issues (problemi critici - tabelle e liste)
        # ...existing code for critical issues...
        
        # Warnings (problemi non critici - elementi di testo)
        empty_text_elements = []
        
        # Paragrafi
        total_empty_p = empty_counts['paragraphs']['empty'] + empty_counts['paragraphs']['whitespace']
        if total_empty_p > 0:
            desc = f"{total_empty_p} paragraphs"
            if empty_counts['paragraphs']['whitespace'] > 0:
                desc += f" ({empty_counts['paragraphs']['whitespace']} with only spaces)"
            empty_text_elements.append(desc)
            
        # Headings
        total_empty_h = empty_counts['headings']['empty'] + empty_counts['headings']['whitespace']
        if total_empty_h > 0:
            desc = f"{total_empty_h} headings"
            if empty_counts['headings']['whitespace'] > 0:
                desc += f" ({empty_counts['headings']['whitespace']} with only spaces)"
            empty_text_elements.append(desc)
            
        # Spans
        total_empty_spans = empty_counts['spans']['empty'] + empty_counts['spans']['whitespace']
        if total_empty_spans > 0:
            desc = f"{total_empty_spans} spans"
            if empty_counts['spans']['whitespace'] > 0:
                desc += f" ({empty_counts['spans']['whitespace']} with only spaces)"
            empty_text_elements.append(desc)
            
        if empty_text_elements:
            self.warnings.append(f"Found empty text elements: {', '.join(empty_text_elements)}")
        
        # Calcolo del punteggio - considerando solo issues critiche
        # ...existing code...

    def validate_figures(self, content: List) -> None:
        # Skip if document is not tagged
        if not self.is_tagged:
            self.check_scores['figures'] = 0
            return
            
        figures = []
        figures_without_alt = []
        
        def check_figures(element: Dict, path: str = "") -> None:
            tag = element.get('tag', '')
            current_path = f"{path}/{tag}" if path else tag
            
            if tag == 'Figure':
                figures.append(current_path)
                alt_text = element.get('text', '').strip()
                if not alt_text:
                    figures_without_alt.append(current_path)
            
            # Check children
            for child in element.get('children', []):
                check_figures(child, current_path)
        
        for element in content:
            check_figures(element)
        
        if figures:
            if figures_without_alt:
                self.issues.append(f"Found {len(figures_without_alt)} figures without alt text: {', '.join(figures_without_alt)}")
                self.check_scores['figures'] = 50
            else:
                count = len(figures)
                self.successes.append(f"Found {count} figure{'' if count == 1 else 's'} with alternative text")
                self.check_scores['figures'] = 100
        else:
            self.check_scores['figures'] = 0

    def validate_heading_structure(self, content: List) -> None:
        # Skip if document is not tagged
        if not self.is_tagged:
            self.check_scores['headings'] = 0
            return
            
        headings = []
        
        def collect_headings(element: Dict) -> None:
            tag = element.get('tag', '')
            if tag.startswith('H'):
                try:
                    level = int(tag[1:])
                    headings.append(level)
                except ValueError:
                    pass
            
            for child in element.get('children', []):
                collect_headings(child)
        
        for element in content:
            collect_headings(element)
        
        if headings:
            # Check if first heading is H1
            if headings[0] != 1:
                self.issues.append(f"First heading is H{headings[0]}, should be H1")
            
            # Check heading hierarchy
            prev_level = 1
            for level in headings:
                if level > prev_level + 1:
                    self.issues.append(f"Incorrect heading structure: H{prev_level} followed by H{level}")
                prev_level = level
            
            if not any(self.issues):
                count = len(headings)
                self.successes.append(f"Found {count} heading{'' if count == 1 else 's'} with correct structure")
                self.check_scores['headings'] = 100
            else:
                self.check_scores['headings'] = 50  # Struttura parzialmente corretta
        else:
            self.warnings.append("No headings found in document")
            self.check_scores['headings'] = 0

    def validate_tables(self, content: List) -> None:
        if not self.is_tagged:
            self.check_scores['tables'] = 0
            return
            
        tables = []
        tables_without_headers = []
        empty_tables = []
        tables_with_duplicate_headers = []
        tables_with_proper_headers = []
        tables_with_multiple_header_rows = []
        tables_without_data = []
        
        def is_table_completely_empty(headers, rows) -> bool:
            # Check if all headers are empty
            all_headers_empty = all(
                not (isinstance(cell, dict) and cell.get('text', '').strip() or
                     isinstance(cell, str) and cell.strip())
                for row in headers
                for cell in row
            )
            
            # Check if all rows are empty
            all_rows_empty = all(
                not (isinstance(cell, dict) and cell.get('text', '').strip() or
                     isinstance(cell, str) and cell.strip())
                for row in rows
                for cell in row
            )
            
            return all_headers_empty and all_rows_empty
        
        def has_duplicate_headers(headers) -> tuple[bool, list]:
            if not headers:
                return False, []
            
            header_texts = []
            duplicates = []
            
            for row in headers:
                row_texts = []
                for cell in row:
                    if isinstance(cell, dict):
                        text = cell.get('text', '').strip()
                    else:
                        text = str(cell).strip()
                    if text in row_texts:
                        duplicates.append(text)
                    row_texts.append(text)
                header_texts.extend(row_texts)
            
            return bool(duplicates), duplicates
        
        def check_tables(element: Dict, path: str = "") -> None:
            tag = element.get('tag', '')
            
            if tag == 'Table':
                table_num = len(tables) + 1
                table_content = element.get('content', {})
                headers = table_content.get('headers', [])
                rows = table_content.get('rows', [])
                
                # First check if table is structurally empty
                if not headers and not rows:
                    empty_tables.append(f"Table {table_num}")
                    return
                # Then check if table has structure but all cells are empty
                elif is_table_completely_empty(headers, rows):
                    empty_tables.append(f"Table {table_num}")
                else:
                    tables.append(f"Table {table_num}")
                    
                    # Check if table has headers
                    if not headers:
                        tables_without_headers.append(f"Table {table_num}")
                    else:
                        # Check number of header rows
                        if len(headers) > 1:
                            tables_with_multiple_header_rows.append((f"Table {table_num}", len(headers)))
                        
                        # Check for duplicate headers
                        has_duplicates, duplicate_values = has_duplicate_headers(headers)
                        if has_duplicates:
                            tables_with_duplicate_headers.append((f"Table {table_num}", duplicate_values))
                        else:
                            tables_with_proper_headers.append(f"Table {table_num}")
                    
                    # Check if table has data rows
                    if not rows:
                        tables_without_data.append(f"Table {table_num}")
            
            # Check children
            for child in element.get('children', []):
                check_tables(child)
        
        for element in content:
            check_tables(element)
        
        # Report issues and warnings
        if empty_tables:
            self.issues.append(f"Found empty tables: {', '.join(empty_tables)}")
        
        if tables:  # Solo se ci sono tabelle non vuote
            # Issues per tabelle senza header o senza dati
            if tables_without_headers:
                self.issues.append(f"Found tables without headers: {', '.join(tables_without_headers)}")
            if tables_without_data:
                self.issues.append(f"Found tables without data rows: {', '.join(tables_without_data)}")
            
            # Warning per tabelle con più righe di intestazione
            for table_id, num_rows in tables_with_multiple_header_rows:
                self.warnings.append(f"{table_id} has {num_rows} header rows, consider using a single header row")
            
            # Report successo per ogni tabella corretta individualmente
            for table_id in tables_with_proper_headers:
                if (not any(table_id == t[0] for t in tables_with_multiple_header_rows) and
                    table_id not in tables_without_data):
                    self.successes.append(f"{table_id} has proper header tags")
                
            # Warning per contenuti duplicati
            if tables_with_duplicate_headers:
                for table_id, duplicates in tables_with_duplicate_headers:
                    self.warnings.append(f"{table_id} has duplicate headers: {', '.join(duplicates)}")
        
        if not (empty_tables or tables_without_headers or tables_without_data):
            self.check_scores['tables'] = 100
        else:
            self.check_scores['tables'] = 50

    def validate_possible_unordered_lists(self, content: List) -> None:
        """Check for consecutive paragraphs starting with '-' that might be unordered lists"""
        if not self.is_tagged:
            self.check_scores['lists'] = 0
            return
            
        def find_consecutive_dash_paragraphs(elements: List, path: str = "") -> List[List[str]]:
            sequences = []
            current_sequence = []
            
            for element in elements:
                if element['tag'] == 'P':
                    text = element.get('text', '').strip()
                    if text.startswith('-'):
                        current_sequence.append(text)
                    else:
                        if len(current_sequence) >= 2:
                            sequences.append(current_sequence.copy())
                        current_sequence = []
                
                # Check children recursively
                if element.get('children'):
                    nested_sequences = find_consecutive_dash_paragraphs(element['children'])
                    sequences.extend(nested_sequences)
            
            # Add last sequence if it exists
            if len(current_sequence) >= 2:
                sequences.append(current_sequence)
                
            return sequences
        
        sequences = find_consecutive_dash_paragraphs(content)
        
        if sequences:
            for sequence in sequences:
                self.warnings.append(
                    f"Found sequence of {len(sequence)} paragraphs that might form an unordered list"
                )
            self.check_scores['lists'] = 50
        else:
            self.check_scores['lists'] = 100

    def validate_possible_ordered_lists(self, content: List) -> None:
        """Check for consecutive paragraphs starting with sequential numbers that might be ordered lists"""
        if not self.is_tagged:
            self.check_scores['lists'] = 0
            return
            
        def find_consecutive_numbered_paragraphs(elements: List, path: str = "") -> List[List[str]]:
            sequences = []
            current_sequence = []
            
            def extract_leading_number(text: str) -> tuple[bool, int]:
                """Extract leading number from text (handles formats like '1.', '1)', '1 ')"""
                import re
                match = re.match(r'^(\d+)[.). ]', text)
                if match:
                    return True, int(match.group(1))
                return False, 0
            
            for element in elements:
                current_path = f"{path}/{element['tag']}" if path else element['tag']
                
                if element['tag'] == 'P':
                    text = element.get('text', '').strip()
                    is_numbered, number = extract_leading_number(text)
                    
                    if is_numbered:
                        if not current_sequence or number == current_sequence[-1][2] + 1:
                            current_sequence.append((current_path, text, number))
                        else:
                            if len(current_sequence) >= 2:
                                sequences.append(current_sequence.copy())
                            current_sequence = []
                            if number == 1:
                                current_sequence.append((current_path, text, number))
                    else:
                        if len(current_sequence) >= 2:
                            sequences.append(current_sequence.copy())
                        current_sequence = []
                
                # Check children recursively
                if element.get('children'):
                    nested_sequences = find_consecutive_numbered_paragraphs(element.get('children'), current_path)
                    sequences.extend(nested_sequences)
            
            # Add last sequence if it exists
            if len(current_sequence) >= 2:
                sequences.append(current_sequence)
                
            return sequences
        
        sequences = find_consecutive_numbered_paragraphs(content)
        
        if sequences:
            for sequence in sequences:
                numbers = [str(p[2]) for p in sequence]
                self.warnings.append(
                    f"Found sequence of {len(numbers)} numbered paragraphs ({', '.join(numbers)}) that might form an ordered list"
                )
            self.check_scores['lists'] = 50
        else:
            self.check_scores['lists'] = 100

    def validate_misused_unordered_lists(self, content: List) -> None:
        """Check for unordered lists containing consecutive numbered items"""
        if not self.is_tagged:
            self.check_scores['lists'] = 0
            return
            
        def extract_leading_number(text: str) -> tuple[bool, int]:
            """Extract number from text even after bullet points"""
            import re
            # Prima rimuovi eventuali bullet points (•, -, *)
            text = re.sub(r'^[•\-*]\s*', '', text.strip())
            # Poi cerca il numero
            match = re.match(r'^(\d+)[.). ]', text)
            if match:
                return True, int(match.group(1))
            return False, 0
        
        def check_list_items(element: Dict, path: str = "") -> None:
            tag = element.get('tag', '')
            current_path = f"{path}/{tag}" if path else tag
            
            if tag == 'L' and not element.get('ordered', False):  # Solo liste non ordinate
                items = element.get('items', [])
                if items:
                    current_sequence = []
                    
                    for item in items:
                        is_numbered, number = extract_leading_number(item)
                        if is_numbered:
                            if not current_sequence or number == current_sequence[-1][1] + 1:
                                current_sequence.append((item, number))
                            else:
                                if len(current_sequence) >= 2:
                                    numbers = [str(item[1]) for item in current_sequence]
                                    self.warnings.append(
                                        f"Found consecutive items numbered {', '.join(numbers)} in unordered list at: {current_path}"
                                    )
                                current_sequence = [(item, number)] if number == 1 else []
                    
                    # Check last sequence
                    if len(current_sequence) >= 2:
                        numbers = [str(item[1]) for item in current_sequence]
                        self.warnings.append(
                            f"Found consecutive items numbered {', '.join(numbers)} in unordered list at: {current_path}"
                        )
            
            # Check children recursively
            for child in element.get('children', []):
                check_list_items(child, current_path)
        
        for element in content:
            check_list_items(element)
        
        if not any(self.warnings):
            self.check_scores['lists'] = 100
        else:
            self.check_scores['lists'] = 50

    def validate_excessive_underscores(self, content: List) -> None:
        """Check recursively for excessive consecutive underscores that might be used for underlining"""
        def check_underscores(text: str) -> tuple[bool, int]:
            """Returns (has_excessive_underscores, count)"""
            import re
            # Cerca sequenze di 4 o più underscore
            pattern = r'_{4,}'
            match = re.search(pattern, text)
            if match:
                return True, len(match.group(0))
            return False, 0
            
        def check_element(element: Dict, path: str = "") -> None:
            current_path = f"{path}/{element['tag']}" if path else element['tag']
            
            # Controlla il testo dell'elemento corrente
            if 'text' in element:
                text = element.get('text', '')
                has_underscores, count = check_underscores(text)
                if has_underscores:
                    self.warnings.append(f"Found {count} consecutive underscores in {current_path} - might be attempting to create underlining")
            
            # Controlla i figli
            for child in element.get('children', []):
                check_element(child, current_path)
            
            # Per le tabelle, controlla le celle
            if element.get('tag') == 'Table':
                table_content = element.get('content', {})
                # Controlla headers
                for i, row in enumerate(table_content.get('headers', [])):
                    for j, cell in enumerate(row):
                        if isinstance(cell, dict):
                            text = cell.get('text', '')
                            has_underscores, count = check_underscores(text)
                            if has_underscores:
                                self.warnings.append(f"Found {count} consecutive underscores in {current_path}/header[{i}][{j}] - might be attempting to create underlining")
                
                # Controlla rows
                for i, row in enumerate(table_content.get('rows', [])):
                    for j, cell in enumerate(row):
                        if isinstance(cell, dict):
                            text = cell.get('text', '')
                            has_underscores, count = check_underscores(text)
                            if has_underscores:
                                self.warnings.append(f"Found {count} consecutive underscores in {current_path}/row[{i}][{j}] - might be attempting to create underlining")
            
            # Per le liste, controlla gli items
            if element.get('tag') == 'L':
                for i, item in enumerate(element.get('items', [])):
                    has_underscores, count = check_underscores(item)
                    if has_underscores:
                        self.warnings.append(f"Found {count} consecutive underscores in {current_path}/item[{i}] - might be attempting to create underlining")
                
        for element in content:
            check_element(element)
        
        if not any(self.warnings):
            self.check_scores['underlining'] = 100
        else:
            self.check_scores['underlining'] = 50

    def validate_spaced_capitals(self, content: List) -> None:
        """Check for words written with spaced capital letters like 'C I T T À'"""
        import re
        
        def is_spaced_capitals(text: str) -> bool:
            # Trova sequenze di lettere maiuscole separate da spazi dove ogni lettera è isolata
            # Es: "C I T T À" match, "CITTÀ" no match, "DETERMINA NOMINA" no match
            pattern = r'(?:^|\s)([A-ZÀÈÌÒÙ](?:\s+[A-ZÀÈÌÒÙ]){2,})(?:\s|$)'
            matches = re.finditer(pattern, text)
            spaced_words = []
            
            for match in matches:
                # Verifica che non ci siano lettere consecutive senza spazio
                word = match.group(1)
                if all(c == ' ' or (c.isupper() and c.isalpha()) for c in word):
                    spaced_words.append(word.strip())
                    
            return spaced_words
            
        def check_element(element: Dict, path: str = "") -> None:
            current_path = f"{path}/{element['tag']}" if path else element['tag']
            
            # Controlla il testo dell'elemento corrente
            if 'text' in element:
                text = element.get('text', '')
                spaced_words = is_spaced_capitals(text)
                if spaced_words:
                    for word in spaced_words:
                        self.warnings.append(f"Found spaced capital letters in {current_path}: '{word}'")
            
            # Controlla i figli
            for child in element.get('children', []):
                check_element(child, current_path)
            
            # Per le tabelle, controlla le celle
            if element.get('tag') == 'Table':
                table_content = element.get('content', {})
                # Controlla headers
                for i, row in enumerate(table_content.get('headers', [])):
                    for j, cell in enumerate(row):
                        if isinstance(cell, dict):
                            text = cell.get('text', '')
                            spaced_words = is_spaced_capitals(text)
                            if spaced_words:
                                for word in spaced_words:
                                    self.warnings.append(f"Found spaced capital letters in {current_path}/header[{i}][{j}]: '{word}'")
                
                # Controlla rows
                for i, row in enumerate(table_content.get('rows', [])):
                    for j, cell in enumerate(row):
                        if isinstance(cell, dict):
                            text = cell.get('text', '')
                            spaced_words = is_spaced_capitals(text)
                            if spaced_words:
                                for word in spaced_words:
                                    self.warnings.append(f"Found spaced capital letters in {current_path}/row[{i}][{j}]: '{word}'")
            
            # Per le liste, controlla gli items
            if element.get('tag') == 'L':
                for i, item in enumerate(element.get('items', [])):
                    spaced_words = is_spaced_capitals(item)
                    if spaced_words:
                        for word in spaced_words:
                            self.warnings.append(f"Found spaced capital letters in {current_path}/item[{i}]: '{word}'")
                
        for element in content:
            check_element(element)
        
        if not any(self.warnings):
            self.check_scores['spacing'] = 100
        else:
            self.check_scores['spacing'] = 50

    def validate_extra_spaces(self, content: List) -> None:
        """Check for excessive spaces that might be used for layout purposes"""
        import re
        
        def check_spaces(text: str) -> List[tuple[str, int]]:
            """Returns list of (space_sequence, count) for suspicious spaces"""
            issues = []
            
            # Cerca sequenze di 3 o più spazi non a inizio/fine riga
            for match in re.finditer(r'(?<!^)\s{3,}(?!$)', text):
                space_seq = match.group()
                issues.append((space_seq, len(space_seq)))
            
            # Cerca tabulazioni multiple
            for match in re.finditer(r'\t{2,}', text):
                tab_seq = match.group()
                issues.append((tab_seq, len(tab_seq)))
            
            return issues
            
        def check_element(element: Dict, path: str = "") -> None:
            current_path = f"{path}/{element['tag']}" if path else element['tag']
            
            # Controlla il testo dell'elemento
            if 'text' in element:
                text = element.get('text', '')
                space_issues = check_spaces(text)
                if space_issues:
                    for space_seq, count in space_issues:
                        self.warnings.append(
                            f"Found {count} consecutive spaces in {current_path} - might be attempting layout with spaces"
                        )
            
            # Controlla i figli
            for child in element.get('children', []):
                check_element(child, current_path)
            
            # Controlli speciali per tabelle
            if element.get('tag') == 'Table':
                table_content = element.get('content', {})
                # Controlla headers
                for i, row in enumerate(table_content.get('headers', [])):
                    for j, cell in enumerate(row):
                        if isinstance(cell, dict):
                            text = cell.get('text', '')
                            space_issues = check_spaces(text)
                            if space_issues:
                                for space_seq, count in space_issues:
                                    self.warnings.append(
                                        f"Found {count} consecutive spaces in {current_path}/header[{i}][{j}]"
                                    )
                
                # Controlla rows
                for i, row in enumerate(table_content.get('rows', [])):
                    for j, cell in enumerate(row):
                        if isinstance(cell, dict):
                            text = cell.get('text', '')
                            space_issues = check_spaces(text)
                            if space_issues:
                                for space_seq, count in space_issues:
                                    self.warnings.append(
                                        f"Found {count} consecutive spaces in {current_path}/row[{i}][{j}]"
                                    )
            
            # Controlli speciali per liste
            if element.get('tag') == 'L':
                for i, item in enumerate(element.get('items', [])):
                    space_issues = check_spaces(item)
                    if space_issues:
                        for space_seq, count in space_issues:
                            self.warnings.append(
                                f"Found {count} consecutive spaces in {current_path}/item[{i}]"
                            )
                
        for element in content:
            check_element(element)
        
        if not any(self.warnings):
            self.check_scores['extra_spaces'] = 100
        else:
            extra_spaces_count = sum(1 for w in self.warnings if "consecutive spaces" in w)
            if extra_spaces_count > 10:
                self.check_scores['extra_spaces'] = 0  # Molti problemi di spaziatura
            else:
                self.check_scores['extra_spaces'] = 50  # Alcuni problemi di spaziatura

    def calculate_weighted_score(self) -> float:
        """Calcola il punteggio pesato di accessibilità"""
        total_weight = sum(self.check_weights.values())
        weighted_sum = sum(
            self.check_weights[check] * self.check_scores[check]
            for check in self.check_weights
        )
        return round(weighted_sum / total_weight, 2)

    def generate_json_report(self) -> Dict:
        return {
            "validation_results": {
                "issues": self.issues,
                "warnings": self.warnings,
                "successes": self.successes,
                "weighted_score": self.calculate_weighted_score(),
                "detailed_scores": {
                    check: score for check, score in self.check_scores.items()
                }
            }
        }

    def print_console_report(self) -> None:
        print("\n📖 Accessibility Validation Report\n")
        
        if self.successes:
            print("✅ Successes:")
            for success in self.successes:
                print(f"  • {success}")
        
        if self.warnings:
            print("\n⚠️  Warnings:")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        if self.issues:
            print("\n❌ Issues:")
            for issue in self.issues:
                print(f"  • {issue}")
        
        # Print summary with weighted score
        total = len(self.successes) + len(self.warnings) + len(self.issues)
        weighted_score = self.calculate_weighted_score()
        
        print(f"\n📊 Summary:")
        print(f"  • Total checks: {total}")
        print(f"  • Successes: {len(self.successes)} ✅")
        print(f"  • Warnings: {len(self.warnings)} ⚠️")
        print(f"  • Issues: {len(self.issues)} ❌")
        print(f"  • Weighted Accessibility Score: {weighted_score}%")
        
        # Overall assessment
        if weighted_score >= 90:
            print("\n🎉 Excellent! Document has very good accessibility.")
        elif weighted_score >= 70:
            print("\n👍 Good! Document has decent accessibility but could be improved.")
        elif weighted_score >= 50:
            print("\n⚠️  Fair. Document needs accessibility improvements.")
        else:
            print("\n❌ Poor. Document has serious accessibility issues.")

def analyze_pdf(pdf_path: str, options: dict) -> None:
    """
    Analyze a PDF file with configurable outputs
    """
    try:
        # Setup output directory
        output_dir = Path(options['output_dir']) if options['output_dir'] else Path(pdf_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        pdf_name = Path(pdf_path).stem

        # Show conversion message only if saving JSON outputs
        if (options['save_full'] or options['save_simple']) and not options['quiet']:
            print("🔄 Converting PDF to JSON structure...", file=sys.stderr)
        
        # Convert PDF to JSON
        pdf_json = pdf_to_json(pdf_path)
        
        # Extract and simplify content
        if 'StructTreeRoot' not in pdf_json:
            if not options['quiet']:
                print("⚠️  Warning: No structure tree found in PDF", file=sys.stderr)
            results = []
        else:
            results = extract_content(pdf_json['StructTreeRoot'])
        
        # Create simplified JSON
        simplified_json = create_simplified_json(pdf_json, results)
        
        # Save full JSON if requested
        if options['save_full']:
            full_path = output_dir / f"{pdf_name}_full.json"
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(pdf_json, f, indent=2, ensure_ascii=False)
            if not options['quiet']:
                print(f"💾 Full JSON saved to: {full_path}")

        # Save simplified JSON if requested
        if options['save_simple']:
            simplified_path = output_dir / f"{pdf_name}_simplified.json"
            with open(simplified_path, 'w', encoding='utf-8') as f:
                json.dump(simplified_json, f, indent=2, ensure_ascii=False)
            if not options['quiet']:
                print(f"💾 Simplified JSON saved to: {simplified_path}")

        # Show document structure if requested
        if options['show_structure']:
            print("\n📄 Document Structure:")
            print("Note: Colors are used to highlight different tag types and do not indicate errors:")
            print(f"  {COLOR_GREEN}[P]{COLOR_RESET}: Paragraphs")
            print(f"  {COLOR_RED}[H1-H6]{COLOR_RESET}: Headings")
            print(f"  {COLOR_ORANGE}[Figure]{COLOR_RESET}: Images")
            print(f"  {COLOR_PURPLE}[Table]{COLOR_RESET}: Tables")
            print(f"  {COLOR_BLUE}[List]{COLOR_RESET}: Lists")
            print("-" * 40)
            for element in simplified_json.get('content', []):
                print_formatted_content(element)
            print("-" * 40)

        # Run validation if requested
        if options['save_report'] or options['show_validation']:
            if not options['quiet']:
                print("\n🔍 Running accessibility validation...")
            
            validator = AccessibilityValidator()
            validator.validate_metadata(simplified_json.get('metadata', {}))
            validator.validate_empty_elements(simplified_json.get('content', []))
            validator.validate_figures(simplified_json.get('content', []))
            validator.validate_heading_structure(simplified_json.get('content', []))
            validator.validate_tables(simplified_json.get('content', []))  # Add table validation
            validator.validate_possible_unordered_lists(simplified_json.get('content', []))  # Add this
            validator.validate_possible_ordered_lists(simplified_json.get('content', []))    # Add this
            validator.validate_misused_unordered_lists(simplified_json.get('content', []))  # Add this
            # Aggiungi i nuovi validatori
            validator.validate_excessive_underscores(simplified_json.get('content', []))
            validator.validate_spaced_capitals(simplified_json.get('content', []))
            validator.validate_extra_spaces(simplified_json.get('content', []))
            
            # Show validation results if requested
            if options['show_validation']:
                validator.print_console_report()
            
            # Save validation report if requested
            if options['save_report']:
                report_path = output_dir / f"{pdf_name}_validation_report.json"
                with open(report_path, 'w', encoding='utf-8') as f:
                    json.dump(validator.generate_json_report(), f, indent=2)
                if not options['quiet']:
                    print(f"\n💾 Validation report saved to: {report_path}")
        
        if not options['quiet']:
            print("\n✨ Analysis complete!")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

def download_pdf(url: str) -> Path:
    """Download a PDF file from URL and save it to a temporary file"""
    try:
        # Validate URL
        parsed = urllib.parse.urlparse(url)
        if not all([parsed.scheme, parsed.netloc]):
            raise ValueError("Invalid URL")

        # Create temporary file
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        tmp_path = Path(tmp.name)

        # Download file
        urllib.request.urlretrieve(url, tmp_path)
        
        return tmp_path

    except Exception as e:
        raise Exception(f"Failed to download PDF: {str(e)}")

def is_url(path: str) -> bool:
    """Check if the given path is a URL"""
    try:
        parsed = urllib.parse.urlparse(path)
        return all([parsed.scheme, parsed.netloc])
    except:
        return False

def main():
    parser = argparse.ArgumentParser(
        description='PDF Analysis Tool: Convert to JSON and validate accessibility',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Basic usage (shows full analysis by default)
  ./analyze_pdf.py document.pdf
  
  Analyze remote PDF via URL
  ./analyze_pdf.py https://example.com/document.pdf
  
  Save reports to specific directory
  ./analyze_pdf.py document.pdf -o /path/to/output --report --simple
  
  Save all files without console output
  ./analyze_pdf.py document.pdf --full --simple --report --quiet
"""
    )
    
    parser.add_argument('input', help='Input PDF file or URL')
    parser.add_argument('--output-dir', '-o', help='Output directory for JSON files')
    
    # File output options
    parser.add_argument('--full', action='store_true', help='Save full JSON output')
    parser.add_argument('--simple', action='store_true', help='Save simplified JSON output')
    parser.add_argument('--report', action='store_true', help='Save validation report')
    
    # Display options
    parser.add_argument('--show-structure', action='store_true', help='Show document structure in console')
    parser.add_argument('--show-validation', action='store_true', help='Show validation results in console')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress all console output except errors')
    
    args = parser.parse_args()
    
    try:
        # Handle URL input
        if is_url(args.input):
            if not args.quiet:
                print("📥 Connecting to remote source...", file=sys.stderr)
            input_path = download_pdf(args.input)
            cleanup_needed = True
        else:
            # Handle local file
            input_path = Path(args.input)
            cleanup_needed = False

        if not input_path.is_file():
            print(f"❌ Error: Input file '{args.input}' does not exist", file=sys.stderr)
            sys.exit(1)
        
        # If no display options specified, enable both structure and validation display
        show_structure = args.show_structure
        show_validation = args.show_validation
        if not any([args.show_structure, args.show_validation, args.quiet]):
            show_structure = True
            show_validation = True
        
        # Prepare options dictionary
        options = {
            'output_dir': args.output_dir,
            'save_full': args.full,
            'save_simple': args.simple,
            'save_report': args.report,
            'show_structure': show_structure,
            'show_validation': show_validation,
            'quiet': args.quiet
        }
        
        analyze_pdf(str(input_path), options)

        # Cleanup temporary file if needed
        if cleanup_needed:
            input_path.unlink()
            
    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
