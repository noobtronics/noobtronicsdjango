<template>
  <div >

  </div>
</template>

<script>
export default {
  name: 'Product_Page',
  data: function () {
    return {

    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="sass">


.prodcontainer
  background-color: hsl(217, 71%, 33%)
  color: white
  padding: 1rem

  h1
    &.title
      color: white
      margin: 0
      font-size: 1.3rem

  .categorylinks
    margin: 0.5rem 0
    padding: 0.2rem 0
    line-height: 0.7rem

    span
      display: inline
      font-size: 0.7rem
      margin: 0


      a
        color: white




.prodpagecolumns
  margin: 0 !important
  padding: 0
  align-items: stretch

  .column
    padding: 0



.prodmainphoto
  margin: 0
  padding: 0
  background-color: hsl(217, 71%, 33%)
  margin-bottom: 0px !important
  height: 18rem



  .photocolumn
    margin: 0
    padding: 0
    padding-right: 1%
    display: flex
    justify-content: center
    align-items: center



    figure
      width: calc(100% - 5px)
      max-width: 18rem


    img
      object-fit: contain
      margin: 0

  .showcasecolumn
    overflow-y: auto
    width: 22%
    display: flex
    align-items: center
    flex-wrap: wrap

    &::-webkit-scrollbar
      width: 0
      background: transparent

    figure
      margin: 0.2rem 0
      border: 1px solid rgba(255,255,255,0.6)



.productdescription
  color: white

  padding-top: 0.5rem
  padding-bottom: 0.7rem

  #prodh1
    font-size: 1.3rem
  #add-to-cart
    font-weight: bold
  #productprice
    font-size: 1.8rem

  h1
    margin: 0
    color: white
    text-align: center

  .field

    .label
      width: 6rem
      margin: 0 auto
      color: white
      text-align: center

      &:hover
        cursor: pointer

      img
        width: 16px
        display: inline


  .variants
    .subtitle
      color: white
      margin: 0
      margin-top: 0.5rem
      text-align: center
    .buttons
      margin-top: 0.2rem

      .button
        height: 2rem
        padding: 0 0.3rem

  .content
    margin: 0
  .content.is-medium
    font-size: 1rem

  .level
    margin: 0
    margin-top: 0.7rem
    margin-bottom: 0.4rem

  p
    color: white
    font-size: 1rem

  .subtitle strong
    color: white
    font-size: 1.5rem

  .delinfo
    text-align: center
    font-size: 0.8rem
    margin-top: 5px


.prodblog
        font-size: 1rem

        .hero-body
          padding: 0.5rem 0.5rem
          color: #333333

          .container
            background-color: #fafafa
            padding: 0.5rem 1rem
            padding-bottom: 2rem

            .content
              table
                width: auto

                td, th
                  border: 1px dashed hsl(217, 71%, 33%)

              .table.is-striped tbody tr:not(.is-selected):nth-child(odd)
                background-color: #d8f5ff

              .table.is-striped tbody tr:not(.is-selected):nth-child(even), th
                background-color: #fafafa

            h2
              font-size: 1.1rem
              padding-top: 1rem

              &:not(:first-child)
                border-top: 1px dashed #e5e5e5

            h3
              font-size: 1rem
              margin-top: 1rem


@import "bulma/sass/utilities/_all.sass"
@import "./../assets/mobile-mixin.sass"

+desktop
  .prodcontainer
    margin-top: 10px
    padding: 10px
    max-width: 1000px

  .prodmainphoto
    padding-left: calc(50% - 193px)
    padding-right: calc(50% - 182px)

    .showcasecolumn
      width: 83px !important
      padding: 2px
      padding-right: 6px
      padding-left: 12px


+mobile
  .prodmainphoto
    .showcasecolumn
      width: 80px !important
      padding: 2px
      padding-right: 4px
      padding-left: 12px


+iphone
  .prodmainphoto
    .showcasecolumn
      width: 83px !important
      padding: 2px
      padding-right: 6px
      padding-left: 12px


+iphone_plus
  .prodmainphoto
    padding-left: calc(50% - 193px)
    padding-right: calc(50% - 182px)

    .showcasecolumn
      width: 83px !important
      padding: 2px
      padding-right: 6px
      padding-left: 12px


</style>
