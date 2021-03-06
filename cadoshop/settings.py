from cadocms import Settings as BaseSettings

class Settings(BaseSettings):
    @property
    def INSTALLED_APPS(self): 
        return super(Settings, self).INSTALLED_APPS + (
                'cadoshop',
                'plata.payment',
                'plata.shop',
                'plata.contact', # Not strictly required (contact model can be exchanged)
                'plata.discount',
                'imagekit',
        )

    PLATA_SHOP_PRODUCT = 'cadoshop.ProductOption'
            
    GRAPPELLI_INDEX_DASHBOARD = 'cadoshop.dashboard.CustomIndexDashboard'
    
    POSTFINANCE = {
        'PSPID': 'plataTEST',
        'SHA1_IN': 'plataSHA1_IN',
        'SHA1_OUT': 'plataSHA1_OUT',
        'LIVE': False,
        }
    
    PAYPAL = {
        'BUSINESS': 'example@paypal.com',
        'LIVE': False,
        }
    
    GRAPPELLI_ADMIN_TITLE = 'Cado Shop Admin'
    
    CURRENCIES = ('PLN',)
    
    PLATA_REPORTING_ADDRESSLINE = 'Example Corp. - 3. Example Street - 1234 Example'

    @property
    def HAYSTACK_CONNECTIONS(self):
        return {
            'default': {
                        'ENGINE': 'cadoshop.search.solr_grouping_backend.GroupedSolrEngine',
                        'URL': 'http://127.0.0.1:8080/solr/' + self.CADO_PROJECT + '/',
                        },
            }