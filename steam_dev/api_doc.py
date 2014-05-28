api_root_api_doc = """
##IF you want to use this API, You have to sign up a dev account.

##Get your `api_token` and `secret_token`

##All api return data charset is `utf-8`, content type is `application/json`

##Detailed usage instructions, please refer to the following link.

--------------------------------------------------------------------------

POST use curl :

    curl -k https://sqa.swim-fish.info/steam/dev/api/steam_user_list
         -H "Content-Type: application/json"
         -d '{
                "api_token":"Your_Api_Token",
                "secret_token":"Your_Secret_Token"
             }'

`-k` for https \n
`-H` Http Head \n
`-d` POST DATA \n

--------------------------------------------------------------------------

###ERROR CODE:
<table class="table table-striped">
  <tr>
    <th>POST Type</th>
    <th>ERROR CODE</th>
    <th>Representation</th>
  </tr>
  <tr>
    <td rowspan="3">application/json</td>
    <td>"detail": "JSON parse error - Expecting value:..."</td>
    <td>JSON format is wrong</td>
  </tr>
  <tr>
    <td>"detail": "FORBIDDEN"</td>
    <td><code>api_token</code> or <code>secret_token</code> not correct</td>
  </tr>
  <tr>
    <td>"detail": "Method 'GET' not allowed."</td>
    <td>GET not allowed</td>
  </tr>
  <tr>
    <td>application/x-www-form-urlencoded</td>
    <td>"detail": "NO POST DATA"</td>
    <td>POST Data is empty</td>
  </tr>
  <tr>
    <td>multipart/form-data</td>
    <td>"detail": "Multipart form parse error - Invalid Content-Type: application/x-www-form-urlencoded"</td>
    <td>Multipart form format is wrong</td>
  </tr>
</table>

"""

###########################################################################
###########################################################################
###########################################################################
###########################################################################


SteamUserList_api_doc = """
List all steam user.
--------------------------------------------------------------------------

POST your dev `api_token` and `secret_token` :

    {
        "api_token" : "Your_Api_Token",
        "secret_token" : "Your_Secret_Token"
    }

If is correct will return:

    [
        {
            "first_name": "",
            "last_name": "",
            "nick_name": "",
            "cell_phone": "",
            "sex": "",
            "photo": "/media/noImageAvailable300.png",
            "api_token": "...",
            "secret_token": "...",
            "created": "2014-05-12T03:58:55Z"
        }
    ]

--------------------------------------------------------------------------

##Data Type:<a class="headerlink" href="#data_type" title="Permalink to this headline">¶</a>
<table class="table table-striped">
  <thead>
    <tr>
      <th>Key</th>
      <th>Value Type</th>
      <th>Max length</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td> first_name    </td>
      <td>       string  </td>
      <td> 30           </td>
    </tr>
    <tr>
      <td> last_name     </td>
      <td>       string  </td>
      <td> 30           </td>
    </tr>
    <tr>
      <td> nick_name     </td>
      <td>       string  </td>
      <td> 30           </td>
    </tr>
    <tr>
      <td> cell_phone    </td>
      <td>       string  </td>
      <td> 20           </td>
    </tr>
    <tr>
      <td><a class="reference internal" href="#sex">sex</a></td>
      <td>       string  </td>
      <td> 1            </td>
    </tr>
    <tr>
      <td><a class="reference internal" href="#photo">photo</a></td>
      <td>          url  </td>
      <td> 200          </td>
    </tr>
    <tr>
      <td><a class="reference internal" href="#token">api_token</a></td>
      <td>       string  </td>
      <td> 100          </td>
    </tr>
    <tr>
      <td><a class="reference internal" href="#token">secret_token</a></td>
      <td>       string  </td>
      <td> 100          </td>
    </tr>
    <tr>
      <td><a class="reference internal" href="#created">created</a></td>
      <td>       string  </td>
      <td> 20*           </td>
    </tr>
  </tbody>
</table>

--------------------------------------------------------------------------

###sex:<a class="headerlink" href="#sex" title="Permalink to this headline">¶</a>
<table class="table table-striped">
  <thead>
    <tr>
      <th>     code </th>
      <th> representation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>        F </td>
      <td>        Female </td>
    </tr>
    <tr>
      <td>        M </td>
      <td>          Male </td>
    </tr>
    <tr>
      <td>        O </td>
      <td>         Other </td>
    </tr>
  </tbody>
</table>

--------------------------------------------------------------------------

###photo:<a class="headerlink" href="#photo" title="Permalink to this headline">¶</a>
example photo_path: `/media/noImageAvailable300.png`

domain url: `https://sqa.swim-fish.info` + photo_path

Location is: `https://sqa.swim-fish.info/media/noImageAvailable300.png`

--------------------------------------------------------------------------

###token:<a class="headerlink" href="#token" title="Permalink to this headline">¶</a>
length 100

composition: `a`to`z` or `0`to`9`

--------------------------------------------------------------------------

###created:<a class="headerlink" href="#created" title="Permalink to this headline">¶</a>
example: `2014-05-13T15:44:05Z`

**year**`-`**month**`-`**day**`T`**hour**`:`**minute**`:`**second**`Z`


<table class="table table-striped">
  <thead>
    <tr>
      <th> time unit </th>
      <th>    number length </th>
      <th> example </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>      year </td>
      <td>                4  </td>
      <td>    2014 </td>
    </tr>
    <tr>
      <td>     month </td>
      <td>                2  </td>
      <td>      05 </td>
    </tr>
    <tr>
      <td>       day </td>
      <td>                2  </td>
      <td>      13 </td>
    </tr>
    <tr>
      <td>      hour </td>
      <td> 2 (24-hour clock) </td>
      <td>      15 </td>
    </tr>
    <tr>
      <td>    minute </td>
      <td>                2  </td>
      <td>      44 </td>
    </tr>
    <tr>
      <td>    second </td>
      <td>                2  </td>
      <td>      05 </td>
    </tr>
  </tbody>
</table>

"""


###########################################################################
###########################################################################
###########################################################################
###########################################################################


SteamDeveloperList_api_doc = """
List all steam developer.
--------------------------------------------------------------------------

POST your dev `api_token` and `secret_token` :

    {
        "api_token" : "Your_Api_Token",
        "secret_token" : "Your_Secret_Token"
    }

If is correct will return:

    [
        {
            "first_name": "",
            "last_name": "",
            "address": "",
            "work_phone": "",
            "fax": "",
            "company_name": "",
            "created": "2014-05-12T03:58:55Z"
        }
    ]

--------------------------------------------------------------------------

##Data Type:<a class="headerlink" href="#data_type" title="Permalink to this headline">¶</a>
<table class="table table-striped">
  <thead>
    <tr>
      <th> Key           </th>
      <th> Value Type    </th>
      <th> Max length   </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td> first_name    </td>
      <td>       string  </td>
      <td> 30           </td>
    </tr>
    <tr>
      <td> last_name     </td>
      <td>       string  </td>
      <td> 30           </td>
    </tr>
    <tr>
      <td> address       </td>
      <td>       string  </td>
      <td> 200          </td>
    </tr>
    <tr>
      <td> work_phone    </td>
      <td>       string  </td>
      <td> 20           </td>
    </tr>
    <tr>
      <td> fax           </td>
      <td>       string  </td>
      <td> 20           </td>
    </tr>
    <tr>
      <td> company_name  </td>
      <td>       string  </td>
      <td> 50           </td>
    </tr>
    <tr>
      <td><a class="reference internal" href="#created" >created</a></td>
      <td>         time  </td>
      <td> 20*           </td>
    </tr>
  </tbody>
</table>

--------------------------------------------------------------------------


###created:<a class="headerlink" href="#created" title="Permalink to this headline">¶</a>
example: `2014-05-13T15:44:05Z`

**year**`-`**month**`-`**day**`T`**hour**`:`**minute**`:`**second**`Z`


<table class="table table-striped">
  <thead>
    <tr>
      <th> time unit </th>
      <th>    number length  </th>
      <th> example </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>      year </td>
      <td> 4                 </td>
      <td>    2014 </td>
    </tr>
    <tr>
      <td>     month </td>
      <td> 2                 </td>
      <td>      05 </td>
    </tr>
    <tr>
      <td>       day </td>
      <td> 2                 </td>
      <td>      13 </td>
    </tr>
    <tr>
      <td>      hour </td>
      <td> 2 (24-hour clock) </td>
      <td>      15 </td>
    </tr>
    <tr>
      <td>    minute </td>
      <td> 2                 </td>
      <td>      44 </td>
    </tr>
    <tr>
      <td>    second </td>
      <td> 2                 </td>
      <td>      05 </td>
    </tr>
  </tbody>
</table>

"""

###########################################################################
###########################################################################
###########################################################################
###########################################################################


SteamUserCheck_api_doc = """
List all steam user.
--------------------------------------------------------------------------

POST your dev `api_token` and `secret_token` :

Do not forget the rearmost `,`


    {
        "api_token" : "Your_Api_Token",
        "secret_token" : "Your_Secret_Token",
        "user_api_token": "User_Api_Token",
        "user_secret_token" : "User_Secret_Token"
    }

If is correct will return:

Only one data, without `[` `]`


    {
        "first_name": "",
        "last_name": "",
        "nick_name": "",
        "cell_phone": "",
        "sex": "",
        "photo": "/media/noImageAvailable300.png",
        "api_token": "...",
        "secret_token": "...",
        "created": "2014-05-12T03:58:55Z"
    }

Not found:


    {
        "detail": "not found"
    }


--------------------------------------------------------------------------

##Data Type:<a class="headerlink" href="#data_type" title="Permalink to this headline">¶</a>
<table class="table table-striped">
  <thead>
    <tr>
      <th>Key</th>
      <th>Value Type</th>
      <th>Max length</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td> first_name    </td>
      <td>       string  </td>
      <td> 30           </td>
    </tr>
    <tr>
      <td> last_name     </td>
      <td>       string  </td>
      <td> 30           </td>
    </tr>
    <tr>
      <td> nick_name     </td>
      <td>       string  </td>
      <td> 30           </td>
    </tr>
    <tr>
      <td> cell_phone    </td>
      <td>       string  </td>
      <td> 20           </td>
    </tr>
    <tr>
      <td><a class="reference internal" href="#sex">sex</a></td>
      <td>       string  </td>
      <td> 1            </td>
    </tr>
    <tr>
      <td><a class="reference internal" href="#photo">photo</a></td>
      <td>          url  </td>
      <td> 200          </td>
    </tr>
    <tr>
      <td><a class="reference internal" href="#token">api_token</a></td>
      <td>       string  </td>
      <td> 100          </td>
    </tr>
    <tr>
      <td><a class="reference internal" href="#token">secret_token</a></td>
      <td>       string  </td>
      <td> 100          </td>
    </tr>
    <tr>
      <td><a class="reference internal" href="#created">created</a></td>
      <td>       string  </td>
      <td> 20*           </td>
    </tr>
  </tbody>
</table>

--------------------------------------------------------------------------

###sex:<a class="headerlink" href="#sex" title="Permalink to this headline">¶</a>
<table class="table table-striped">
  <thead>
    <tr>
      <th>     code </th>
      <th> representation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>        F </td>
      <td>        Female </td>
    </tr>
    <tr>
      <td>        M </td>
      <td>          Male </td>
    </tr>
    <tr>
      <td>        O </td>
      <td>         Other </td>
    </tr>
  </tbody>
</table>

--------------------------------------------------------------------------

###photo:<a class="headerlink" href="#photo" title="Permalink to this headline">¶</a>
example photo_path: `/media/noImageAvailable300.png`

domain url: `https://sqa.swim-fish.info` + photo_path

Location is: `https://sqa.swim-fish.info/media/noImageAvailable300.png`

--------------------------------------------------------------------------

###token:<a class="headerlink" href="#token" title="Permalink to this headline">¶</a>
length 100

composition: `a`to`z` or `0`to`9`

--------------------------------------------------------------------------

###created:<a class="headerlink" href="#created" title="Permalink to this headline">¶</a>
example: `2014-05-13T15:44:05Z`

**year**`-`**month**`-`**day**`T`**hour**`:`**minute**`:`**second**`Z`


<table class="table table-striped">
  <thead>
    <tr>
      <th> time unit </th>
      <th>    number length </th>
      <th> example </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>      year </td>
      <td>                4  </td>
      <td>    2014 </td>
    </tr>
    <tr>
      <td>     month </td>
      <td>                2  </td>
      <td>      05 </td>
    </tr>
    <tr>
      <td>       day </td>
      <td>                2  </td>
      <td>      13 </td>
    </tr>
    <tr>
      <td>      hour </td>
      <td> 2 (24-hour clock) </td>
      <td>      15 </td>
    </tr>
    <tr>
      <td>    minute </td>
      <td>                2  </td>
      <td>      44 </td>
    </tr>
    <tr>
      <td>    second </td>
      <td>                2  </td>
      <td>      05 </td>
    </tr>
  </tbody>
</table>

"""
