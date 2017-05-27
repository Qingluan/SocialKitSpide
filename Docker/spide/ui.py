
import tornado.web
import os

class Card(tornado.web.UIModule):
    
    def render(self, title, img_url='images/hat.png', content='...', html=None):
        return self.render_string('template/ui_templates/card.html', 
            title=title, 
            img_url=img_url,
            html=html,
            content=content,
        )

    
    def embedded_css(self):
        return '''
            .card-container {
                background: #ebebeb;
                margin:10px;
                border-radius: 25px; 
            }

            .card-container > .card {
                background: #fafafa;
                border: 2px solid white;
                border-radius: 20px;
                margin: 2px;
            }

            .card > img {
                width: 60px;
                height: 60px;
                float: left;
                margin-right: 30px;
                margin-bottom: 30px;
                padding: 4px;
                border: 2px solid #fff;
                background: rgb(229, 229, 229);

            }
        '''


class Inputs(tornado.web.UIModule):
    """
    type: horizontal/ inline . this will be parse to form-horizontal/ form-inline in bootstrap
    """

    types = (
        'text',
        'file',
        'email',
        'submit',
        'button',
        'checkbox',
        'password',
    )

    def classify(self, name):
        res = name.split(":")
        if len(res) == 2:
            tpe, name = res
            if tpe not in Inputs.types:
                name, v = res
                return ['text', name, v]
            else:
                return [tpe, name, '']
        elif len(res) == 3:
            tpe, name, value = res
            if tpe not in Inputs.types:
                raise Exception("not found input type %s" % tpe)
            return [tpe, name, value]
        elif len(res) == 1:
            return ['text', res[0], '']


    def render(self, *inputs, type='normal', title=None, form_type='horizontal', action='#', method='post'):
        inputs = [ self.classify(input) for input in inputs ]
        return self.render_string('template/ui_templates/{t}_inputs.html'.format(t=type), 
            inputs=inputs,
            type=form_type,
            title=title,
            action=action,
            method=method,
        )


    # def html_body(self):
    #     return '<script>document.write("Hello!")</script>'


class Table(tornado.web.UIModule):

    def rows(self, head_num, items):
        body = [[items[ii*head_num + i] for i in range(head_num)] for ii in range(int(len(items) / head_num ))]
        if len(items) % head_num != 0:
            yu = len(items) % head_num
            all_len = len(items)
            return body + [[items[i] for i in range(all_len - yu, all_len)]]
        return body


    def render(self,table_headers , *table_items, type='normal', title='', table_type='striped'):
        items = self.rows(len(table_headers), table_items)
        return self.render_string('template/ui_templates/{t}_table.html'.format(t=type), 
            headers=table_headers,
            items=items,
            type=table_type,
            title=title,
        )



class Nav(tornado.web.UIModule):
    """
    items example:
        [{
            'txt':'xxx',
            'link': '/index',
            'active': '1',
            'tq': '1'
        },
        {
            'txt':'xxx',
            'link': '/url',

        },
        {
            'txt':'xxx',
            'link': '/index2',
        }]
    """

    def render(self, items, type='normal', title='Dashboard', nav_type='stacked'):
        return self.render_string('template/ui_templates/{t}_nav.html'.format(t=type), 
            items=items,
            type=nav_type,
            title=title,
        )

    def embedded_css(self):
        return '''
.tq{
    padding-left: 15px;
    padding-right: 15px;
    margin-bottom: 5px;
    font-size: 85%;
    font-weight: 100;
    letter-spacing: 1px;
    color: #51586a;
    text-transform: uppercase;
    
}

.nav > li > a{
    position: relative;
    display: block;
    padding: 7px 15px 7px ;
    padding-left: 27px;
    border-radius: 4px;
}

.nav > li.active > a {
    color: #252830;
    background-color: #e5e5e5;
}
li.divider{
    width: 70%;
    align-self: center;
    align-content: center;
    left:10%; 
    height: 1px;
    margin: 9px 1px;*
    margin: -5px 0 5px;
    overflow: hidden;
    bottom:10px;
    background-color: #e5e5e5;
    border-bottom: 1px solid #e5e5e5;    
}
        '''

class Files(Nav):
    """
    items example:
        Files(file_path)
    """
    def get_len(self, f):
        l = os.stat("./static/files/" + f).st_size
        s = "%f B" % float(l)
        if l / 1024 > 1:
            s = "%2.2f KB" % float(l/ 1024)
        else:
            return s

        if l / 1024 ** 2 > 1:
            s = "%2.2f MB" % float(l/ 1024 **2)
        else:
            return s

        if l / 1024 ** 3 > 1:
            s = "%2.2f GB" % float(l/ 1024 **3)
        else:
            return s

    def render(self, type='normal', title='Dashboard', nav_type='stacked'):
        ss = [{
            "txt":f,
            "link":"/static/files/" + f,
            "code": f.split(".").pop() + "[%s]" % self.get_len(f)
        } for f in os.listdir("./static/files")]
        return super().render(ss, type=type, title=title, nav_type=nav_type)


class LMap(tornado.web.UIModule):
    """
    this is a map plugin , based on leaflet
    """
    def render(self, id, host, height=460):
        return self.render_string('template/ui_templates/plugin-map.html', 
            id=id,
            host=host,
            height=height)


class LEarth(tornado.web.UIModule):
    """
    this is a earth plugin , based on leaflet
    """
    def render(self, id, height=360, width=760):
        return self.render_string('template/ui_templates/plugin-earth.html',
            id=id,
            w=width,
            h=height)
        

class LGeoControl(tornado.web.UIModule):
    """
    this is a controller to controll geo.
    """
    def render(self, host="localhost:8080/mapapi", earth="earth",map="lmap"):
        return self.render_string('template/ui_templates/plugin-geo-control.html',
            host=host,
            map=map,
            earth=earth,
        )

        