from scrapy import Spider, Request
from scrapy.loader import ItemLoader
from ..items import ApartmentItem


class DBSspider(Spider):
    name = 'BDSspider'
    # allowed_domains = ['https://batdongsan.com.vn/']

    def start_requests(self):
        # start_url = 'https://batdongsan.com.vn/ban-can-ho-chung-cu-ha-noi'
        # for i in range(1, 886):
        #     yield Request(url=start_url + '/p' + str(i), callback=self.parse_link)

        # one page
        url = 'https://batdongsan.com.vn/ban-can-ho-chung-cu-pho-hoang-cau-phuong-o-cho-dua-prj-d-le-pont-dor-hoang-cau/chinh-chu-ban-gap-tai-du-an-tan-ang-minh-36-ang-98m2-2pn-gia-4-8-ty-lh-0975357268-pr26919881'
        # url = 'https://batdongsan.com.vn/ban-can-ho-chung-cu-duong-5-xa-dong-hoi-prj-eurowindow-river-park/chi-23-7tr-m2-91m2-3pn-2vs-full-noi-that-co-ban-view-nam-h-long-bien-pr28106294'
        yield Request(url=url, callback=self.parse_features)

    def parse_link(self, response):
        # base_url = 'https://batdongsan.com.vn'
        apartment_links = response.xpath('//*[@id="product-lists-web"]/div/a')
        yield from response.follow_all(apartment_links, callback=self.parse_features)

    def parse_features(self, response):
        l = ItemLoader(item=ApartmentItem(), response=response)

        l.add_value('url', response.url)
        l.add_css('title', '#product-detail-web > h1.tile-product::text')
        l.add_css('short_detail', '#product-detail-web > div.short-detail::text')
        l.add_xpath('price', '//*[@id="product-detail-web"]/div[3]/ul/li[contains(span[1]/text(), "giá")]/span[2]/text()')
        l.add_xpath('area', '//*[@id="product-detail-web"]/div[3]/ul/li[contains(span[1]/text(), "Diện tích")]/span[2]/text()')
        l.add_css('description', '.des-product::text')
        l.add_xpath('bedrooms', '//*[@id="product-detail-web"]/div[5]/div[contains(span/text(), "Đặc điểm")]/div/div[contains(span[1]/text(), "phòng ngủ")]/span[2]/text()')
        l.add_xpath('toilets', '//*[@id="product-detail-web"]/div[5]/div[contains(span/text(), "Đặc điểm")]/div/div[contains(span[1]/text(), "toilet")]/span[2]/text()')
        l.add_xpath('address', '//*[@id="product-detail-web"]/div[5]/div[contains(span/text(), "Đặc điểm")]/div/div[contains(span[1]/text(), "Địa chỉ")]/span[2]/text()')
        l.add_xpath('direction', '//*[@id="product-detail-web"]/div[5]/div[contains(span/text(), "Đặc điểm")]/div/div[contains(span[1]/text(), "Hướng nhà")]/span[2]/text()')
        l.add_xpath('balcony_direction', '//*[@id="product-detail-web"]/div[5]/div[contains(span/text(), "Đặc điểm")]/div/div[contains(span[1]/text(), "Hướng ban công")]/span[2]/text()')
        l.add_xpath('furniture', '//*[@id="product-detail-web"]/div[5]/div[contains(span/text(), "Đặc điểm")]/div/div[contains(span[1]/text(), "Nội thất")]/span[2]/text()')
        l.add_xpath('law_doc', '//*[@id="product-detail-web"]/div[5]/div[contains(span/text(), "Đặc điểm")]/div/div[contains(span[1]/text(), "Pháp lý")]/span[2]/text()')
        l.add_xpath('project', '//*[@id="product-detail-web"]/div[5]/div[contains(span/text(), "Thông tin")]/div/div[contains(span[1]/text(), "Tên")]/span[2]/text()[1]')
        l.add_xpath('investor', '//*[@id="product-detail-web"]/div[5]/div[contains(span/text(), "Thông tin")]/div/div[contains(span[1]/text(), "Chủ")]/span[2]/text()[1]')
        l.add_xpath('post_date', '//*[@id="product-detail-web"]/div[5]/div[@class="product-config pad-16"]/ul/li[1]/span[2]/text()')
        l.add_xpath('id', '//*[@id="product-detail-web"]/div[5]/div[@class="product-config pad-16"]/ul/li[contains(span[1]/text(), "Mã")]/span[2]/text()')

        yield l.load_item()
