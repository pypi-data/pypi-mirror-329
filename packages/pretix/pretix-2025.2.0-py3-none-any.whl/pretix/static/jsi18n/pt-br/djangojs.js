

'use strict';
{
  const globals = this;
  const django = globals.django || (globals.django = {});

  
  django.pluralidx = function(n) {
    const v = n > 1;
    if (typeof v === 'boolean') {
      return v ? 1 : 0;
    } else {
      return v;
    }
  };
  

  /* gettext library */

  django.catalog = django.catalog || {};
  
  const newcatalog = {
    "(one more date)": [
      "(mais uma data)",
      "({num} mais datas)"
    ],
    "All": "Todos",
    "An error has occurred.": "Ocorreu um erro.",
    "An error of type {code} occurred.": "Ocorreu um erro do tipo {code}.",
    "Barcode area": "\u00c1rea de c\u00f3digo de barras",
    "Cart expired": "O carrinho expirou",
    "Check-in QR": "QR Check-in",
    "Click to close": "Clique para fechar",
    "Close message": "Fechar mensagem",
    "Comment:": "Coment\u00e1rio:",
    "Contacting Stripe \u2026": "Contatando Stripe\u2026",
    "Copied!": "Copiado!",
    "Count": "Contagem",
    "Do you really want to leave the editor without saving your changes?": "Voc\u00ea realmente quer deixar o editor sem salvar suas mudan\u00e7as?",
    "Error while uploading your PDF file, please try again.": "Erro durante o upload do seu arquivo PDF, tente novamente.",
    "Generating messages \u2026": "Gerando mensagens \u2026",
    "Group of objects": "Grupo de objetos",
    "Marked as paid": "Marcado como pago",
    "None": "Nenhum",
    "Object": "Objeto",
    "Others": "Outros",
    "Paid orders": "Ordens pagas",
    "Placed orders": "Ordens colocadas",
    "Powered by pretix": "Distribu\u00eddo por pretix",
    "Press Ctrl-C to copy!": "Pressione Ctrl+C para copiar!",
    "Saving failed.": "Erro ao salvar.",
    "The PDF background file could not be loaded for the following reason:": "O arquivo de fundo PDF n\u00e3o p\u00f4de ser carregado pelo seguinte motivo:",
    "Ticket design": "Design de bilhetes",
    "Total": "Total",
    "Total revenue": "Rendimento total",
    "Unknown error.": "Erro desconhecido.",
    "Use a different name internally": "Use um nome diferente internamente",
    "We are currently sending your request to the server. If this takes longer than one minute, please check your internet connection and then reload this page and try again.": "Estamos enviando seu pedido para o servidor. Se isso demorar mais de um minuto, verifique sua conex\u00e3o com a internet e, em seguida, recarregue esta p\u00e1gina e tente novamente.",
    "We are processing your request \u2026": "Estamos processando seu pedido \u2026",
    "We currently cannot reach the server, but we keep trying. Last error code: {code}": "Atualmente n\u00e3o podemos acessar o servidor, mas continuamos tentando. \u00daltimo c\u00f3digo de erro: {code}",
    "We currently cannot reach the server. Please try again. Error code: {code}": "N\u00e3o podemos acessar o servidor. Por favor, tente novamente. C\u00f3digo de erro: {code}",
    "Your color has bad contrast for text on white background, please choose a darker shade.": "Sua cor tem um contraste ruim para o texto sobre fundo branco, por favor, escolha um tom mais escuro.",
    "Your color has decent contrast and is probably good-enough to read!": "Sua cor tem um contraste aceit\u00e1vel e provavelmente \u00e9 boa o suficiente para ler!",
    "Your color has great contrast and is very easy to read!": "Sua cor tem grande contraste e \u00e9 muito f\u00e1cil de ler!",
    "widget\u0004Buy": "Comprar",
    "widget\u0004Close": "Fechar",
    "widget\u0004Close ticket shop": "Pausar loja virtual",
    "widget\u0004Continue": "Continuar",
    "widget\u0004FREE": "Gr\u00e1tis",
    "widget\u0004Only available with a voucher": "Dispon\u00edvel apenas com um voucher",
    "widget\u0004Redeem": "Lido",
    "widget\u0004Redeem a voucher": "Voucher j\u00e1 utlizado",
    "widget\u0004Reserved": "Reservado",
    "widget\u0004Resume checkout": "Retomar checkout",
    "widget\u0004Sold out": "Esgotado",
    "widget\u0004The cart could not be created. Please try again later": "O carrinho n\u00e3o pode ser criado. Por favor, tente mais tarde",
    "widget\u0004The ticket shop could not be loaded.": "A loja n\u00e3o pode ser aberta.",
    "widget\u0004Voucher code": "C\u00f3digo do voucher",
    "widget\u0004Waiting list": "Lista de espera",
    "widget\u0004You currently have an active cart for this event. If you select more products, they will be added to your existing cart.": "Voc\u00ea atualmente possui um carrinho ativo para este evento. Se voc\u00ea selecionar mais produtos, eles ser\u00e3o adicionados ao seu carrinho existente.",
    "widget\u0004currently available: %s": "atualmente dispon\u00edvel: %s",
    "widget\u0004from %(currency)s %(price)s": "A partir de %(currency)s %(price)s",
    "widget\u0004incl. %(rate)s% %(taxname)s": "Inclu\u00eddo %(rate)s% %(taxname)s",
    "widget\u0004minimum amount to order: %s": "valor m\u00ednimo por pedido: %s",
    "widget\u0004plus %(rate)s% %(taxname)s": "mais %(rate)s% %(taxname)s"
  };
  for (const key in newcatalog) {
    django.catalog[key] = newcatalog[key];
  }
  

  if (!django.jsi18n_initialized) {
    django.gettext = function(msgid) {
      const value = django.catalog[msgid];
      if (typeof value === 'undefined') {
        return msgid;
      } else {
        return (typeof value === 'string') ? value : value[0];
      }
    };

    django.ngettext = function(singular, plural, count) {
      const value = django.catalog[singular];
      if (typeof value === 'undefined') {
        return (count == 1) ? singular : plural;
      } else {
        return value.constructor === Array ? value[django.pluralidx(count)] : value;
      }
    };

    django.gettext_noop = function(msgid) { return msgid; };

    django.pgettext = function(context, msgid) {
      let value = django.gettext(context + '\x04' + msgid);
      if (value.includes('\x04')) {
        value = msgid;
      }
      return value;
    };

    django.npgettext = function(context, singular, plural, count) {
      let value = django.ngettext(context + '\x04' + singular, context + '\x04' + plural, count);
      if (value.includes('\x04')) {
        value = django.ngettext(singular, plural, count);
      }
      return value;
    };

    django.interpolate = function(fmt, obj, named) {
      if (named) {
        return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
      } else {
        return fmt.replace(/%s/g, function(match){return String(obj.shift())});
      }
    };


    /* formatting library */

    django.formats = {
    "DATETIME_FORMAT": "j \\d\\e F \\d\\e Y \u00e0\\s H:i",
    "DATETIME_INPUT_FORMATS": [
      "%d/%m/%Y %H:%M:%S",
      "%d/%m/%Y %H:%M:%S.%f",
      "%d/%m/%Y %H:%M",
      "%d/%m/%y %H:%M:%S",
      "%d/%m/%y %H:%M:%S.%f",
      "%d/%m/%y %H:%M",
      "%Y-%m-%d %H:%M:%S",
      "%Y-%m-%d %H:%M:%S.%f",
      "%Y-%m-%d %H:%M",
      "%Y-%m-%d"
    ],
    "DATE_FORMAT": "j \\d\\e F \\d\\e Y",
    "DATE_INPUT_FORMATS": [
      "%d/%m/%Y",
      "%d/%m/%y",
      "%Y-%m-%d"
    ],
    "DECIMAL_SEPARATOR": ",",
    "FIRST_DAY_OF_WEEK": 0,
    "MONTH_DAY_FORMAT": "j \\d\\e F",
    "NUMBER_GROUPING": 3,
    "SHORT_DATETIME_FORMAT": "d/m/Y H:i",
    "SHORT_DATE_FORMAT": "d/m/Y",
    "THOUSAND_SEPARATOR": ".",
    "TIME_FORMAT": "H:i",
    "TIME_INPUT_FORMATS": [
      "%H:%M:%S",
      "%H:%M:%S.%f",
      "%H:%M"
    ],
    "YEAR_MONTH_FORMAT": "F \\d\\e Y"
  };

    django.get_format = function(format_type) {
      const value = django.formats[format_type];
      if (typeof value === 'undefined') {
        return format_type;
      } else {
        return value;
      }
    };

    /* add to global namespace */
    globals.pluralidx = django.pluralidx;
    globals.gettext = django.gettext;
    globals.ngettext = django.ngettext;
    globals.gettext_noop = django.gettext_noop;
    globals.pgettext = django.pgettext;
    globals.npgettext = django.npgettext;
    globals.interpolate = django.interpolate;
    globals.get_format = django.get_format;

    django.jsi18n_initialized = true;
  }
};

