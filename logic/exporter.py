import json

class EmbedExporter:
    @staticmethod
    def to_json(data):
        return json.dumps(data, indent=4)

    @staticmethod
    def to_discord_py(data):
        code = f"embed = discord.Embed(\n    title='{data.get('title', '')}',\n"
        code += f"    description='{data.get('description', '')}',\n"
        code += f"    color={data.get('color', 0x2b2d31)}\n)\n"
        
        if data.get('author_name'):
            code += f"embed.set_author(name='{data['author_name']}', icon_url='{data.get('author_icon', '')}')\n"
        
        for field in data.get('fields', []):
            code += f"embed.add_field(name='{field['name']}', value='{field['value']}', inline={field['inline']})\n"
            
        if data.get('image'):
            code += f"embed.set_image(url='{data['image']}')\n"
        
        code += f"embed.set_footer(text='{data.get('footer_text', '')}', icon_url='{data.get('footer_icon', '')}')"
        return code

    @staticmethod
    def to_discord_js(data):
        # Lógica similar para EmbedBuilder do d.js v14
        return "const embed = new EmbedBuilder()..."